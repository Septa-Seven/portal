from rest_framework.routers import SimpleRouter
from apps.teams import views


router = SimpleRouter()

router.register('invitations', views.InvitationViewSet)
router.register('', views.TeamViewSet, basename="teams")

urlpatterns = router.urls
