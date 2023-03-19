from django.urls import path, include
from .views import CustomRegisterView, activate, activation_completed, ChangePasswordView
from django_rest_passwordreset import urls


urlpatterns = [
    path('', CustomRegisterView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('password-reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),
    # path('activate/<uidb64>/<token>', activate, name='activate'),
    # path('activation/completed', activation_completed, name='completed'),
]
