from rest_framework.routers import SimpleRouter
from apps.comments import views


router = SimpleRouter()

router.register('', views.CommentViewSet)

urlpatterns = router.urls
