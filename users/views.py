from rest_framework.views import APIView
from .serializers import RegisterAccountSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from .tasks import activate_email
from .tokens import account_activation_token
from users.models import Account
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken


class CustomRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterAccountSerializer, responses=RegisterAccountSerializer)
    def post(self, request):
        reg_serializer = RegisterAccountSerializer(data=request.data)
        if reg_serializer.is_valid():
            user = Account.objects.create_user(username=reg_serializer.validated_data['username'],
                                               email=reg_serializer.validated_data['email'],
                                               first_name=None,
                                               password=reg_serializer.validated_data['password'],
                                               )
            user.save()
            activate_email.delay(user_username=user.username,
                                 user_id=user.id,
                                 to_email=reg_serializer.validated_data['email'])
            return Response({'message': 'Check your inbox!'})
        #     if new_user:
        #         return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('PATCH', 'GET'))
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user.id, token):
        user.is_active = True
        user.save()

        return HttpResponseRedirect("http://127.0.0.1:3000/completed")
    else:
        return Response({'message': 'Activation link is invalid!'})


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': 'Wrong Password.'},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
