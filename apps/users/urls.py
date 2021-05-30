from rest_framework.routers import SimpleRouter
from apps.users import views


router = SimpleRouter()

router.register('team', views.TeamViewSet)
router.register('invitation', views.InvitationViewSet)

urlpatterns = router.urls
