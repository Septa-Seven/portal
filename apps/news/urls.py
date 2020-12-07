from rest_framework.routers import SimpleRouter
from apps.news import views


router = SimpleRouter()

router.register('', views.NewsViewSet)

urlpatterns = router.urls
