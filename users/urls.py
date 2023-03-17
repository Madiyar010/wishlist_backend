from django.urls import path
from .views import CustomRegisterView, activate, activation_completed


urlpatterns = [
    path('', CustomRegisterView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('activation/completed', activation_completed, name='completed'),
]
