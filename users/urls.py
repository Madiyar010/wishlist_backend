from django.urls import path, include
from .views import CustomRegisterView, activate, ChangePasswordView


urlpatterns = [
    path('', CustomRegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view()),
    path('password-reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),
    path('activate/<uidb64>/<token>', activate, name='activate'),

]
