from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda value: [host.strip() for host in value.split(',')]
)

INTERNAL_IPS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'debug_toolbar',

    'games'
]

JAZZMIN_SETTINGS = {
    'site_title': 'Администрирование каталога',
    'site_header': 'Каталог игр',
    'site_brand': 'Каталог игр',
    'welcome_sign': 'Управление каталогом видеоигр',
    'show_sidebar': True,
    'navigation_expanded': True,
    'order_with_respect_to': [
        'games',
        'games.game',
        'games.developer',
        'games.platform',
        'auth',
        'auth.user',
        'auth.group',
    ],
    'icons': {
        'games': 'fas fa-gamepad',
        'games.game': 'fas fa-dice',
        'games.developer': 'fas fa-user-astronaut',
        'games.platform': 'fas fa-desktop',
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.group': 'fas fa-users',
    },
    'show_ui_builder': False,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://t.me/monk", "new_window": True},
        {"model": "auth.User"},
    ],
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
#  Light themes
    # "theme" : "flatly",
    # "theme" : "simplex",
    # "theme" : "cerulean",
    # "theme" : "cosmo",
    # "theme" : "journal",
    # "theme" : "litera",
    # "theme" : "lumen",
    # "theme" : "lux",
    # "theme" : "materia",
    # "theme" : "minty",
    # "theme" : "pulse",
    # "theme" : "sandstone",
    # "theme" : "simplex",
    # "theme" : "sketchy",
    # "theme" : "spacelab",
    # "theme" : "united",
    # "theme" : "yeti",
    #  Dark themes
    "theme": "darkly",
    # "theme" : "slate",
    # "theme" : "cyborg",
    # "theme" : "solar",
    # "theme" : "superhero",
    # 'mode_theme': 'superhero',
    'navbar_small_text': False,
    'footer_small_text': False,
    'sidebar_nav_small_text': False,
    'sidebar_nav_legacy_style': True,
    'sidebar_nav_flat_style': True,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': True,
    'button_classes': {
        'primary': 'btn-outline-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-info',
        'success': 'btn-success',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
    },
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'games-api-cache',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'games.permissions.IsAdminOrReadOnly',
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'games': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
