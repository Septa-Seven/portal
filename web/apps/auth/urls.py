from django.urls import path, include
from apps.auth.views import GithubLogin, VKLogin, GoogleLogin, YandexLogin


urlpatterns = [
    path('github/', GithubLogin.as_view(), name='github_login'),
    path('vk/', VKLogin.as_view(), name='vk_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('yandex/', YandexLogin.as_view(), name='yandex_login'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
