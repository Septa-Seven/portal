from rest_framework.routers import SimpleRouter
from apps.blog import views


router = SimpleRouter()

router.register('', views.ArticleViewSet)
router.register('', views.CommentViewSet)

urlpatterns = router.urls
