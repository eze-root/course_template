import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor

import test_template


def module_at(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DeploymentTests(unittest.TestCase):
    render = test_template.CourseTemplateTests.render

    def test_docker_only_generation_keeps_its_workflow(self):
        project = self.render(include_docker="yes", deploy_to_github_pages="no")
        self.assertTrue((project / ".github/workflows/docker.yml").is_file())
        self.assertFalse((project / ".github/workflows/pages.yml").exists())

    def test_deploy_transports_config_through_sudo_and_cleans_up_on_failure(self):
        project = self.render(include_docker="yes")
        deploy = module_at(project / "scripts/deploy.py")
        environment = {
            "COURSE_DOMAIN": "course.example.edu",
            "COURSE_DATA_ROOT": "/vol1/courses/$budget # teacher's files",
            "COURSE_DJANGO_SECRET_KEY": "must-not-leak-to-deployment-file",
            "RUNNER_TEMP": str(project),
        }
        for fail in (False, True):
            calls = []
            files = []

            def fake_sudo(command, **kwargs):
                self.assertEqual(command[:4], ["sudo", "docker", "compose", "--env-file"])
                path = Path(command[4])
                files.append(path)
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                content = path.read_text()
                self.assertIn("COURSE_DOMAIN='course.example.edu'", content)
                self.assertIn("$budget # teacher\\'s files", content)
                self.assertNotIn("must-not-leak", content)
                self.assertNotIn("COURSE_DJANGO_SECRET_KEY", content)
                calls.append(command)
                if fail:
                    raise subprocess.CalledProcessError(1, command)

            if fail:
                with self.assertRaises(subprocess.CalledProcessError):
                    deploy.deploy(environment, fake_sudo)
            else:
                deploy.deploy(environment, fake_sudo)
                self.assertEqual(len(calls), 3)
                self.assertEqual(calls[0][-2:], ["config", "--quiet"])
            self.assertTrue(all(not path.exists() for path in files))

    def test_invalid_deploy_values_fail_before_sudo(self):
        project = self.render(include_docker="yes")
        deploy = module_at(project / "scripts/deploy.py")
        for domain in ("", "https://course.edu", "*.course.edu", "course.edu/path", "course.edu:80", "course.edu\nINJECT=1"):
            with self.subTest(domain=domain), self.assertRaises(ValueError):
                deploy.deployment_environment({"COURSE_DOMAIN": domain})
        with self.assertRaises(ValueError):
            deploy.deployment_environment({"COURSE_DOMAIN": "course.edu", "COURSE_DATA_ROOT": "relative"})
        with self.assertRaises(ValueError):
            deploy.dotenv_line("KEY", "value\nANOTHER=1")

    @unittest.skipUnless(os.environ.get("COURSE_COMPOSE_TEST_BINARY"), "optional standalone Compose validation")
    def test_real_compose_after_environment_is_cleared(self):
        project = self.render(include_docker="yes")
        deploy = module_at(project / "scripts/deploy.py")
        values = {"COURSE_DOMAIN": "course.example.edu", "COURSE_DATA_ROOT": "/vol1/$budget # teacher's files"}
        calls = []

        def real_compose_config(command, **kwargs):
            if command[-2:] == ["config", "--quiet"]:
                # Reproduce sudo's removal of COURSE_* while retaining its --env-file.
                clean = {k: v for k, v in os.environ.items() if not k.startswith("COURSE_")}
                result = subprocess.run([os.environ["COURSE_COMPOSE_TEST_BINARY"], *command[3:-2], "config", "--format", "json"],
                                        **kwargs, env=clean, capture_output=True, text=True)
                service = json.loads(result.stdout)["services"]["course-site"]
                self.assertEqual(service["environment"]["COURSE_DOMAIN"], values["COURSE_DOMAIN"])
                # Compose serializes literal '$' as '$$' so config can be reused.
                self.assertEqual(service["volumes"][0]["source"], values["COURSE_DATA_ROOT"].replace("$", "$$"))
                self.assertEqual(service["labels"]["traefik.http.routers.test-course-https.rule"], "Host(`course.example.edu`)")
                self.assertEqual(service["labels"]["traefik.http.services.test-course.loadbalancer.server.port"], "80")
                calls.append(result)

        deploy.deploy(values, real_compose_config)
        self.assertEqual(len(calls), 1)

    def test_django_derives_settings_and_keeps_key_between_workers(self):
        project = self.render(include_docker="yes")
        config = module_at(project / "course_config.py")
        env = {"COURSE_DOMAIN": "course.example.edu", "COURSE_RUNTIME_DATA_DIR": str(project / "data")}
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: config.django_settings(env), range(16)))
        first = results[0]
        self.assertEqual(len({item["SECRET_KEY"] for item in results}), 1)
        self.assertGreaterEqual(len(first["SECRET_KEY"]), 64)
        self.assertEqual(first["ALLOWED_HOSTS"], ["course.example.edu"])
        self.assertEqual(first["CSRF_TRUSTED_ORIGINS"], ["https://course.example.edu"])
        self.assertTrue(first["SESSION_COOKIE_SECURE"])
        self.assertEqual(stat.S_IMODE((project / "data/.django-secret-key").stat().st_mode), 0o600)
        # An independent interpreter represents a restarted container worker.
        result = subprocess.run([sys.executable, "-c", "from course_config import django_settings; print(django_settings()['SECRET_KEY'])"],
                                cwd=project, env={**os.environ, **env}, check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), first["SECRET_KEY"])

    def test_existing_django_secret_and_legacy_origin_are_respected(self):
        project = self.render(include_docker="yes")
        config = module_at(project / "course_config.py")
        env = {"COURSE_PUBLIC_ORIGIN": "https://old.example.edu", "COURSE_DJANGO_SECRET_KEY": "existing-secret",
               "COURSE_RUNTIME_DATA_DIR": str(project / "data")}
        settings = config.django_settings(env)
        self.assertEqual(settings["SECRET_KEY"], "existing-secret")
        self.assertEqual(settings["ALLOWED_HOSTS"], ["old.example.edu"])
        self.assertFalse((project / "data/.django-secret-key").exists())
        with self.assertRaises(ValueError):
            config.django_settings({**env, "COURSE_ALLOWED_HOSTS": "*.example.edu"})
        with self.assertRaises(ValueError):
            config.django_settings({**env, "COURSE_PUBLIC_ORIGIN": "http://old.example.edu"})
        with self.assertRaises(ValueError):
            config.django_settings({"COURSE_RUNTIME_DATA_DIR": str(project / "data")})
