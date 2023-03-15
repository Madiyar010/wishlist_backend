from django.urls import path
from .views import CustomRegisterView, activate


urlpatterns = [
    path('', CustomRegisterView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
