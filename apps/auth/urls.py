from django.urls import path
from apps.auth.views import GithubLogin

urlpatterns = [
    path('github/', GithubLogin.as_view(), name='github_login')
]
