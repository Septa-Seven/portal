from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.yandex.views import YandexAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class CustomSocialLoginView(SocialLoginView):
    callback_route: str = None

    def post(self, request, *args, **kwargs):
        # TODO: Issue: https://github.com/iMerica/dj-rest-auth/issues/275
        try:
            return super().post(request, *args, **kwargs)
        except OAuth2Error:
            raise AuthenticationFailed

    @property
    def callback_url(self):
        domain = self.request.META.get("HTTP_ORIGIN", settings.DOMAIN)
        return domain + self.callback_route


class GithubLogin(CustomSocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_route = '/github_callback'


class VKLogin(CustomSocialLoginView):
    adapter_class = VKOAuth2Adapter
    client_class = OAuth2Client
    callback_route = '/vk_callback'


class GoogleLogin(CustomSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_route = '/google_callback'


class YandexLogin(CustomSocialLoginView):
    adapter_class = YandexAuth2Adapter
    client_class = OAuth2Client
    callback_route = '/yandex_callback'
