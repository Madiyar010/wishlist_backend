from rest_framework import routers
from .views import WishViewSet


router = routers.SimpleRouter()
router.register(r'wishes', WishViewSet, basename='Wishes')
urlpatterns = router.urls
