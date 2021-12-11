from rest_framework.routers import SimpleRouter
from apps.blog import views


router = SimpleRouter()

router.register('articles', views.ArticleViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = router.urls
