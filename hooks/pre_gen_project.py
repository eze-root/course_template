import re
import sys
from datetime import date


PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"
ACCENT_COLOR = "{{ cookiecutter.accent_color }}"
COURSE_START_DATE = "{{ cookiecutter.course_start_date }}"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


if not re.fullmatch(r"[a-z][a-z0-9-]*", PROJECT_SLUG):
    fail("project_slug must start with a lowercase letter and contain only a-z, 0-9, and '-'")

if "--" in PROJECT_SLUG or PROJECT_SLUG.endswith("-"):
    fail("project_slug cannot contain consecutive or trailing hyphens")

if not re.fullmatch(r"\d+\.\d+", PYTHON_VERSION):
    fail("python_version must look like '3.13'")

if not re.fullmatch(r"#[0-9a-fA-F]{6}", ACCENT_COLOR):
    fail("accent_color must be a six-digit hex color such as '#d95c41'")

try:
    date.fromisoformat(COURSE_START_DATE)
except ValueError:
    fail("course_start_date must be an ISO date such as '2026-09-01'")
