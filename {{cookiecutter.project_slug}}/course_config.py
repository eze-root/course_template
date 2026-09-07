"""Optional Django settings adapter; this static template does not install Django.

In a future backend's settings.py: globals().update(django_settings()).
The application's other settings (apps, middleware, URLs) remain its responsibility.
"""
import os
from pathlib import Path
import re
import secrets
import tempfile
from urllib.parse import urlsplit


def persistent_key(directory):
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / ".django-secret-key"
    if not target.exists():
        fd, temporary = tempfile.mkstemp(prefix=".key-", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="ascii") as stream:
                stream.write(secrets.token_urlsafe(48))
                stream.flush()
                os.fsync(stream.fileno())
            try:
                # Atomic publish: concurrent workers keep the same complete key.
                os.link(temporary, target)
            except FileExistsError:
                pass
        finally:
            Path(temporary).unlink(missing_ok=True)
    value = target.read_text(encoding="ascii").strip()
    if not value:
        raise ValueError("Persistent Django key is empty; restore it from backup")
    return value


def django_settings(environ=None):
    environ = os.environ if environ is None else environ
    debug = environ.get("COURSE_DEBUG", "0").lower() in ("1", "true", "yes")
    domain = environ.get("COURSE_DOMAIN", "").strip()
    origin = environ.get("COURSE_PUBLIC_ORIGIN", "").strip()
    if not origin:
        if domain:
            origin = "https://" + domain
        elif debug:
            origin = "http://localhost:8000"
        else:
            raise ValueError("Production requires COURSE_DOMAIN or COURSE_PUBLIC_ORIGIN")
    parsed = urlsplit(origin)
    hostname = parsed.hostname or ""
    if (parsed.scheme not in (("http", "https") if debug else ("https",))
            or not hostname or parsed.username or parsed.password
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment
            or not all(re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", part)
                       for part in hostname.split("."))):
        raise ValueError("COURSE_PUBLIC_ORIGIN must be a single HTTPS origin; no path or wildcard")
    # Evaluating port rejects malformed values before creating any files.
    parsed.port
    origin = origin.rstrip("/")
    if domain and hostname != domain.lower():
        raise ValueError("COURSE_DOMAIN and COURSE_PUBLIC_ORIGIN must use the same host")
    allowed = [v.strip() for v in environ.get("COURSE_ALLOWED_HOSTS", "").split(",") if v.strip()]
    if not allowed:
        allowed = [hostname] + (["127.0.0.1"] if debug and hostname == "localhost" else [])
    if any("*" in host for host in allowed):
        raise ValueError("Use an exact COURSE_ALLOWED_HOSTS value or .example.edu, not *.example.edu")
    csrf = [v.strip() for v in environ.get("COURSE_CSRF_TRUSTED_ORIGINS", "").split(",") if v.strip()] or [origin]
    data = Path(environ.get("COURSE_RUNTIME_DATA_DIR") or ("data" if debug else "/data"))
    database = Path(environ.get("COURSE_DB_PATH") or str(data / "course.sqlite3"))
    media = Path(environ.get("COURSE_MEDIA_ROOT") or str(data / "uploads"))
    database.parent.mkdir(parents=True, exist_ok=True)
    media.mkdir(parents=True, exist_ok=True)
    key = environ.get("COURSE_DJANGO_SECRET_KEY") or persistent_key(data)
    return {
        "DEBUG": debug,
        "SECRET_KEY": key,
        "ALLOWED_HOSTS": allowed,
        "CSRF_TRUSTED_ORIGINS": csrf,
        "DATABASES": {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": database}},
        "MEDIA_ROOT": media,
        "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
        "SESSION_COOKIE_SECURE": not debug,
        "CSRF_COOKIE_SECURE": not debug,
        "SECURE_SSL_REDIRECT": not debug,
        "SECURE_HSTS_SECONDS": int(environ.get("COURSE_HSTS_SECONDS") or ("0" if debug else "31536000")),
    }
