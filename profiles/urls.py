from rest_framework import routers
from .views import ProfileViewSet


router = routers.SimpleRouter()
router.register(r'', ProfileViewSet, basename='Profiles')
urlpatterns = router.urls
