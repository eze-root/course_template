"""Deploy with sudo without losing Actions environment variables.

Requires only Python's standard library on the self-hosted runner.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def deployment_environment(environ):
    domain = environ.get("COURSE_DOMAIN", "").strip()
    if not domain or len(domain) > 253 or not all(
        re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
        for label in domain.split(".")
    ):
        raise ValueError("Set COURSE_DOMAIN to a hostname without https://, path or wildcard")
    data_root = environ.get("COURSE_DATA_ROOT", "").strip()
    if data_root and (not Path(data_root).is_absolute() or ":" in data_root):
        raise ValueError("COURSE_DATA_ROOT must be an absolute Docker host directory without ':'")
    port = environ.get("COURSE_PORT", "").strip() or "8080"
    if not port.isdigit() or not 1 <= int(port) <= 65535:
        raise ValueError("COURSE_PORT must be between 1 and 65535")
    return {"COURSE_DOMAIN": domain.lower(), "COURSE_DATA_ROOT": data_root, "COURSE_PORT": port}


def dotenv_line(name, value):
    # Compose single quotes preserve literal $, #, backslashes and whitespace.
    if any(char in value for char in "\r\n\0"):
        raise ValueError(f"{name} must be a single-line value")
    return name + "='" + value.replace("'", "\\'") + "'\n"


def deploy(environ=None, run=None):
    environ = os.environ if environ is None else environ
    run = subprocess.run if run is None else run
    values = deployment_environment(environ)
    # mkstemp creates a unique file with mode 0600, including concurrent runs.
    fd, filename = tempfile.mkstemp(prefix="course-compose-", suffix=".env", dir=environ.get("RUNNER_TEMP") or None)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            for name, value in values.items():
                stream.write(dotenv_line(name, value))
        command = ["sudo", "docker", "compose", "--env-file", filename,
                   "-f", str(ROOT / "docker-compose.yml"),
                   "-f", str(ROOT / "docker-compose.traefik.yml")]
        # Quiet config validation prevents printing any future secrets into logs.
        run(command + ["config", "--quiet"], cwd=ROOT, check=True)
        run(command + ["up", "-d", "--build", "--wait", "--wait-timeout", "120", "--remove-orphans"], cwd=ROOT, check=True)
        run(command + ["ps"], cwd=ROOT, check=True)
    finally:
        Path(filename).unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        deploy()
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
