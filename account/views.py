from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRSerializer, UserLSerializer, ProfileSerializer,PasChSerializer,SPS, UPRS
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh':str(refresh), 'access': str(refresh.access_token)}

class Registration(APIView):
    renderer_classes = [UserRenderer]
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
                token = get_tokens_for_user(user)
            if user:
                return Response({'token':token,'msg':'set user success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(reg_serializer.errors, status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserLSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":"Success Login"}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)


class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = PasChSerializer(data=request.data,context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password change'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SPRE(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer= SPS(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset email send'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UPRV(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UPRS(data = request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
