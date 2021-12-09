from rest_framework.routers import SimpleRouter
from apps.teams import views


router = SimpleRouter()

router.register('', views.TeamViewSet)
router.register('invitations', views.InvitationViewSet)

urlpatterns = router.urls
