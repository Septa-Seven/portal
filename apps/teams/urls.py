from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.teams import views


router = SimpleRouter()

router.register('', views.TeamViewSet)
router.register('invitation', views.InvitationViewSet)

urlpatterns = router.urls
