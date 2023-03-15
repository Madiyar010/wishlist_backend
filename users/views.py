from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterAccountSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class CustomRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterAccountSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
