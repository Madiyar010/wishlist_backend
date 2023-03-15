from rest_framework.views import APIView
from .serializers import RegisterAccountSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .tasks import activate_email
from .tokens import account_activation_token
from users.models import Account
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes


class CustomRegisterView(APIView):
    permission_classes = [AllowAny]

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
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user.id, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Activation completed!'})

    else:
        return Response({'message': 'Activation link is invalid!'})
