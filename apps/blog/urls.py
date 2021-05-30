from rest_framework.routers import SimpleRouter
from apps.blog import views


router = SimpleRouter()

router.register('article', views.ArticleViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = router.urls
