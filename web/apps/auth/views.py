from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.yandex.views import YandexAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class CatchOAuth2ErrorSocialLoginView(SocialLoginView):
    def post(self, request, *args, **kwargs):
        # TODO: Issue: https://github.com/iMerica/dj-rest-auth/issues/275
        try:
            return super().post(request, *args, **kwargs)
        except OAuth2Error:
            raise AuthenticationFailed


class GithubLogin(CatchOAuth2ErrorSocialLoginView):

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.GITHUB_CALLBACK_URL


class VKLogin(CatchOAuth2ErrorSocialLoginView):
    adapter_class = VKOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.VK_CALLBACK_URL


class GoogleLogin(CatchOAuth2ErrorSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.GOOGLE_CALLBACK_URL


class YandexLogin(CatchOAuth2ErrorSocialLoginView):
    adapter_class = YandexAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.YANDEX_CALLBACK_URL
