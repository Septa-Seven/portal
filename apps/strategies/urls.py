from rest_framework.routers import SimpleRouter
from apps.strategies import views

router = SimpleRouter()
router.register('', views.StrategyViewSet)

urlpatterns = router.urls
