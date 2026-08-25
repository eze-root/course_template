import ast
import tempfile
import unittest
from pathlib import Path

from cookiecutter.main import cookiecutter


REPO_ROOT = Path(__file__).resolve().parents[1]


class CourseTemplateTests(unittest.TestCase):
    def render(self, **overrides: str) -> Path:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        context = {
            "project_name": "Test Course",
            "project_slug": "test-course",
            "initialize_git": "no",
            **overrides,
        }
        config_file = Path(tempdir.name) / "cookiecutter-config.yaml"
        config_file.write_text(
            "cookiecutters_dir: {0}/templates\n"
            "replay_dir: {0}/replay\n"
            "default_context: {{}}\n".format(tempdir.name),
            encoding="utf-8",
        )
        output = cookiecutter(
            str(REPO_ROOT),
            no_input=True,
            output_dir=tempdir.name,
            extra_context=context,
            config_file=str(config_file),
        )
        return Path(output)

    def test_minimal_project_removes_optional_files(self) -> None:
        project = self.render(
            deploy_to_github_pages="no",
            include_docker="no",
            include_pdf="no",
        )
        self.assertFalse((project / ".github").exists())
        self.assertFalse((project / "Dockerfile").exists())
        self.assertFalse((project / "scripts/build_pdf.sh").exists())
        conf = (project / "source/conf.py").read_text(encoding="utf-8")
        ast.parse(conf)

    def test_full_project_keeps_optional_files(self) -> None:
        project = self.render(
            deploy_to_github_pages="yes",
            include_docker="yes",
            include_pdf="yes",
        )
        expected = [
            ".github/workflows/pages.yml",
            "Dockerfile",
            "docker-compose.yml",
            "scripts/build_pdf.sh",
        ]
        for relative_path in expected:
            self.assertTrue((project / relative_path).is_file(), relative_path)
        conf = (project / "source/conf.py").read_text(encoding="utf-8")
        ast.parse(conf)

    def test_rendered_project_has_core_course_sections(self) -> None:
        project = self.render()
        for relative_path in [
            "source/index.md",
            "source/lectures/index.md",
            "source/labs/index.md",
            "source/assignments/index.md",
            "source/resources/index.md",
            "AGENTS.md",
            "README.md",
        ]:
            self.assertTrue((project / relative_path).is_file(), relative_path)

        pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('name = "test-course"', pyproject)

        agents = (project / "AGENTS.md").read_text(encoding="utf-8")
        for required_rule in [
            "# 课程项目协作约定",
            "## 内容组织",
            "## 工具链",
            "## 文档工作流",
            "## Git 与变更范围",
            "## 完成标准",
            "frontmatter",
            "uv run make clean",
            "学生隐私数据",
        ]:
            self.assertIn(required_rule, agents)

    def test_english_page_titles_are_valid_quoted_yaml(self) -> None:
        project = self.render(language="en")
        lecture = (project / "source/lectures/lesson-01-introduction.md").read_text(
            encoding="utf-8"
        )
        self.assertIn('title: "Lecture 1: Introduction"', lecture)

    def test_current_course_site_baseline_is_retained(self) -> None:
        project = self.render(include_docker="yes")

        conf = (project / "source/conf.py").read_text(encoding="utf-8")
        self.assertIn("source-sans-3VF.css", conf)
        self.assertIn('"globaltoc_expand_depth": 2', conf)

        css = (project / "source/_static/css/src/site.css").read_text(
            encoding="utf-8"
        )
        for expected in [
            '"Source Sans 3 VF"',
            "--course-globaltoc-width: 20rem",
            ".yue table",
            "div.admonition",
            ".sy-breadcrumbs a",
        ]:
            self.assertIn(expected, css)

        dockerfile = (project / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("uv run --no-sync python -m sphinx", dockerfile)
        self.assertIn("HEALTHCHECK", dockerfile)
        self.assertNotIn("sphinx -M dirhtml source build -W", dockerfile)


if __name__ == "__main__":
    unittest.main()
