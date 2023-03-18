from rest_framework import routers
from .views import WishViewSet, search_wishes
from django.urls import path


router = routers.SimpleRouter()
router.register(r'wishes', WishViewSet, basename='Wishes')
urlpatterns = [
    path('search/<str:query>', search_wishes, name='search_wishes'),
]
urlpatterns += router.urls
