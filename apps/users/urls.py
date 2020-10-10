from django.urls import path
from apps.users.views import UserDetail

urlpatterns = [
    path('', UserDetail.as_view()),
]
