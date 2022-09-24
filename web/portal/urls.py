from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


api_urlpatterns = [
    path('teams/', include('apps.teams.urls')),
    path('blog/', include('apps.blog.urls')),
    path('matchmaking/', include('apps.matchmaking.urls')),
    path('auth/', include('apps.auth.urls')),
    path('users/', include('apps.users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('accounts/', include('allauth.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
