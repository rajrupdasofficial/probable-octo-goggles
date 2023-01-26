from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRSerializer, UserLSerializer
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
# Create your views here.

class Registration(APIView):
    def post(self,request,format=None):
        reg_serializer = UserRSerializer(data=request.data)
        if reg_serializer.is_valid(raise_exception=True):
            password = reg_serializer.validated_data.get('password')
            password2 = reg_serializer.validated_data.get('password2')
            if password != password2:
                return Response({'msg':'passwords not matched'})
            else:
                reg_serializer.validated_data['password']=make_password(password)
                user = reg_serializer.save()
            if user:
                return Response({'msg':'set user success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(reg_serializer.errors, status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request,format=None):
        serializer = UserLSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                return Response({"msg":"Success Login"}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)


