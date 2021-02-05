from rest_framework.routers import SimpleRouter
from apps.articles import views


router = SimpleRouter()

router.register('', views.ArticleViewSet)

urlpatterns = router.urls
