from pathlib import Path
import shutil
import stat
import subprocess


PROJECT_ROOT = Path.cwd()


def remove(path: str) -> None:
    target = PROJECT_ROOT / path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


if "{{ cookiecutter.deploy_to_github_pages }}" != "yes":
    remove(".github")

if "{{ cookiecutter.include_docker }}" != "yes":
    remove("Dockerfile")
    remove("docker-compose.yml")
    remove(".dockerignore")

if "{{ cookiecutter.include_pdf }}" != "yes":
    remove("scripts/build_pdf.sh")

for script in (PROJECT_ROOT / "scripts").glob("*.sh"):
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

if "{{ cookiecutter.initialize_git }}" == "yes":
    git = shutil.which("git")
    if git:
        result = subprocess.run(
            [git, "init", "--quiet", "-b", "main"],
            cwd=PROJECT_ROOT,
            check=False,
        )
        if result.returncode != 0:
            print("WARNING: git initialization failed; initialize the repository manually.")
    else:
        print("WARNING: git was not found; initialize the repository manually.")

print()
print("Course project created successfully.")
print("Next steps:")
print("  1. cd {{ cookiecutter.project_slug }}")
print("  2. uv sync")
print("  3. npm install")
print("  4. uv run make dirhtml")
