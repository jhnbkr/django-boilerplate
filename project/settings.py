import os
from pathlib import Path

import environ

from project import __version__

BASE_DIR: Path = Path(__file__).resolve().parent.parent

env = environ.Env()
dotenv_path: str = os.environ.get("DJANGO_DOTENV_PATH", os.path.join(BASE_DIR, ".env"))
if dotenv_path and os.path.exists(dotenv_path):
    env.read_env(dotenv_path)

INSTALLED_APPS: list[str] = [
    "proxy.apps.ProxyConfig",
]

MIDDLEWARE: list[str] = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": env.db(),
}

CACHE_ENABLED: bool = env.bool("CACHE_ENABLED", default=True)
if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": env.str("REDIS_URL"),
            "KEY_PREFIX": env.str("CACHE_KEY_PREFIX", default=""),
            "TIMEOUT": env.int("DEFAULT_CACHE_TIMEOUT", 60 * 5),
        }
    }
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS", default=[], cast=str)
DEBUG: bool = env.bool("DEBUG", default=False)
SECRET_KEY: str = env.str("SECRET_KEY")
SECURE_SSL_REDIRECT: bool = env.bool("SECURE_SSL_REDIRECT", default=True)

WSGI_APPLICATION: str = "project.wsgi.application"
ROOT_URLCONF: str = "project.urls"
APPEND_SLASH: bool = False
STRIP_SLASH: bool = True

LANGUAGE_CODE: str = "en-us"
USE_I18N: bool = False

ENVIRONMENT: str = env.str("ENVIRONMENT", default="undefined")
VERSION: str = ".".join(str(value) for value in __version__)


NINJA_PAGINATION_CLASS: str = "api.pagination.LimitOffsetPagination"
PAGINATION_DEFAULT_PAGE_LIMIT: int = env.int(
    "PAGINATION_DEFAULT_PAGE_LIMIT",
    default=10,
)
PAGINATION_MAX_PAGE_LIMIT: int = env.int(
    "PAGINATION_MAX_PAGE_LIMIT",
    default=100,
)
