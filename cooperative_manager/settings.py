import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv  # Додано для зчитування .env

# Завантажуємо змінні з .env файлу
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- БЕЗПЕКА (Security) ---

# Беремо SECRET_KEY з .env. Якщо його немає — використовуємо старий (тільки для розробки)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-f$4n(87jt61zfe(o@n(md3cbgrd$z-6lx$13b(s!@h1z1yds-d')

# DEBUG тепер залежить від .env. За замовчуванням False для безпеки на сервері
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Список хостів зчитуємо з .env (через кому)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# --- Визначення додатків ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Ваші додатки
    'users',
    'cooperatives',
    'staff',
    'meters',
    'rest_framework',
    'rest_framework.authtoken',
]

# Налаштування DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Додано для статики на AWS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cooperative_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'cooperative_manager.wsgi.application'

# --- База даних (PostgreSQL) ---
# Використовує DATABASE_URL з вашого .env у Docker

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3'),
        conn_max_age=600
    )
}

# --- Паролі та валідація ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Інтернаціоналізація ---

LANGUAGE_CODE = 'uk-ua'  # Змінено на українську
TIME_ZONE = 'Europe/Kyiv'  # Встановлено ваш часовий пояс
USE_I18N = True
USE_TZ = True

# --- Статичні та Медіа файли ---

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка, куди Docker збиратиме статику
STATICFILES_DIRS = [BASE_DIR / "static"]

# Налаштування для фото лічильників мешканців
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Налаштування WhiteNoise для стиснення статики
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Авторизація ---

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'user_dashboard'
LOGOUT_REDIRECT_URL = '/'