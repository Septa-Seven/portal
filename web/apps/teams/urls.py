from rest_framework.routers import SimpleRouter
from apps.teams import views


router = SimpleRouter()

router.register('invitations', views.InvitationViewSet)
router.register('', views.TeamViewSet)

urlpatterns = router.urls
