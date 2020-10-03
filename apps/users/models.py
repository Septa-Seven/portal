from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


# docstring в трех двойных ковычках.
# Более информативные и обезличенные комментарии и названия
# Соответсвующее REST наименование ресурсов https://restfulapi.net/resource-naming/
# С абсолюными импортами более понятна структура приложения https://www.python.org/dev/peps/pep-0008/#imports
# Главная модель - User, а UserProfile просто таблица с данными User. Все остальные модели должны ссылаться на User.
# В User уже есть date_joined, убран дубликат в UserProfile.
# Использовать Djoser, чтобы сделать ViewSet для User.
# Проект небольшой, поэтому для фронтендера будет намного легче делать запросы к api без версий
# Пользовательская модель пользователя рекомендуется в докментации джанги https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Намного сложнее работать с несколькими моделями и при использовании djoser все равно пришлось бы создавать вместе с пользователем его профиль, а для этого нужно переопределять UserManager, поэтому в любом случае не получится без определения пользовательской модели
