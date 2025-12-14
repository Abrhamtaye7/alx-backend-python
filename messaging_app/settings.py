import os
from pathlib import Path
from dotenv import load_dotenv

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "messaging_db"),
        "USER": os.getenv("MYSQL_USER", "messaging_user"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "messaging_password"),
        "HOST": os.getenv("MYSQL_HOST", "db"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key")
