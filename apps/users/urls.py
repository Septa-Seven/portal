from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.users import views


router = SimpleRouter()

router.register('teams', views.TeamViewSet)
router.register('invitation', views.InvitationViewSet)

urlpatterns = router.urls + [
    path('me/team', views.DetailUser.as_view())
]
