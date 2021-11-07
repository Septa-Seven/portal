# Run locally in docker

Build backend with local development config:
```commandline
docker-compose -f docker-compose.dev.yml build
```

Collect static files and run migrations:
```commandline
docker-compose -f docker-compose.dev.yml run septa-backend python manage.py collectstatic
docker-compose -f docker-compose.dev.yml run septa-backend python manage.py migrate
```

Run in detach mode:
```commandline
docker-compose -f docker-compose.dev.yml up -d
```

Create superuser without input (see [environment variables](#superuser))
```commandline
docker-compose -f docker-compose.dev.yml run septa-backend python manage.py createsuperuser --no-input
```


# Environment variables

<<<<<<< HEAD
Store environment variables in **_.env_** file or in shell.

## [Django settings](https://docs.djangoproject.com/en/3.1/ref/settings/)

### Core

```dotenv
DEBUG=True
SECRET_KEY=<string>
```

### Email

```dotenv
EMAIL_HOST=<string>
EMAIL_HOST_USER=<string>
EMAIL_HOST_PASSWORD=<string>
EMAIL_PORT=<int>
```

### Superuser

Provide credentials to create superuser without input.

```dotenv
DJANGO_SUPERUSER_USERNAME=<>
DJANGO_SUPERUSER_EMAIL=<>
DJANGO_SUPERUSER_PASSWORD=<>
```

## Database (PostgreSQL)

```dotenv
DB_NAME=<Database name>
DB_USER=<Database user>
DB_PASSWORD=<Database password>
DB_HOST=<Database host>
DB_PORT=<Database port>
```

## Djoser

Djoser uses [django-templated-mail](https://django-templated-mail.readthedocs.io/en/latest/settings.html) as mailing backend.

```dotenv
DOMAIN=<Frontend domain>
```
Djoser uses [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) as JWT token library.

```dotenv
ACCESS_TOKEN_LIFETIME=15
```

## AWS S3 serving

To use AWS S3 as media and static storage make sure **USE_AWS_S3** is True and
settings to connect to AWS is provided. [Django S3 storage]() is used as
backend storage.

```dotenv
USE_AWS_S3=True

AWS_REGION=<>
AWS_ACCESS_KEY_ID=<>
AWS_SECRET_ACCESS_KEY=<>
AWS_S3_BUCKET_NAME=<>
```

## Filesystem serving

When runned locally **BACKEND_DOMAIN** settings responsible
for media url construction.

_MEDIA_URL = BACKEND_DOMAIN + /media/_

```dotenv
BACKEND_DOMAIN=<>
```
=======

>>>>>>> articles+comments
