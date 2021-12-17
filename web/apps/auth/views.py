from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GithubLogin(SocialLoginView):
    # TODO: Handle issue: https://github.com/iMerica/dj-rest-auth/issues/275
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.GITHUB_CALLBACK_URL


class VKLogin(SocialLoginView):
    adapter_class = VKOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.VK_CALLBACK_URL


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return settings.GOOGLE_CALLBACK_URL
