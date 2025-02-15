from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializer import UserRegisterSerializer, UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,UserSendResetPasswordEmailSerializer,UserResetPasswordSerializer
from django.contrib.auth import authenticate
from user.renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegisterationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({"token":token,"message":"registeration successfull."},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email,password=password)
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({"token":token,"message":"Login successfull."},status=status.HTTP_200_OK)
      else:
        return Response({"errors":{'non_field_errors':["Email and Password is not Valide"]}},status=status.HTTP_404_NOT_FOUND)  
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
  
 
class UserProfileView(APIView):  
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self,request,format=None):
    serializer = UserChangePasswordSerializer(data=request.data,context = {'user':request.user})
    if serializer.is_valid(raise_exception=True):
      return Response({'message':'password chnaged successfully'},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
class UserSendResetPasswordEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = UserSendResetPasswordEmailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      return Response({'message':'Password Reset Link send to your Email'},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

  
class UserResetPasswordView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,uid,token,format=None):
    serializer = UserResetPasswordSerializer(data = request.data,context={'uid':uid,'token':token})
    if serializer.is_valid(raise_exception=True):
      return Response({'message':'Password Reset Successfull'},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    