from django.urls import path
from .views import CustomRegisterView


urlpatterns = [
    path('', CustomRegisterView.as_view()),
]
