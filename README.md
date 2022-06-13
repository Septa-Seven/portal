# Run locally in docker

Build backend with local development config:
```commandline
docker-compose build
```

Collect static files and run migrations:
```commandline
docker-compose run web python manage.py migrate
docker-compose run web python manage.py collectstatic
```

Run in detach mode:
```commandline
docker-compose up -d
```

Create superuser without input (see [environment variables](#superuser))
```commandline
docker-compose run web python manage.py createsuperuser --no-input
```


# Environment variables

Store environment variables in **_.env_** file or in shell.

## [Django settings](https://docs.djangoproject.com/en/4.0/ref/settings/)

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
AWS_S3_ENDPOINT_URL=<>
```

## Filesystem serving

When runned locally **BACKEND_DOMAIN** settings responsible
for media url construction.

_MEDIA_URL = BACKEND_DOMAIN + /media/_

```dotenv
BACKEND_DOMAIN=<>
```