from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

# Create your views here.
class UserRegistration(APIView):
  def post(self,request):
    serializer = RegisterSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'User created successfully.'},status= status.HTTP_201_CREATED)

class UserLogin(APIView):
  
  def post(self,request):
    username = request.data.get('username')    
    password = request.data.get('password')  
    user = authenticate(username = username, password = password)
    if user is not None:      
      token, created= Token.objects.get_or_create(user = user)
      return Response({ "message": "Login successful",
                        "token": token.key,
                        "username": user.username,
                        "role": user.role})
    return Response({'error': 'Invalid Credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class ForgotPasswordAPIView(APIView):
  def post(self,request):
    serializer = ForgotPasswordSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user = User.objects.filter(email = email,is_active = True).first()
    if user and user.has_usable_password():
      token = default_token_generator.make_token(user)
      send_mail('Forgot password',
                f'Your password reset token is : {token}',
                settings.DEFAULT_FROM_EMAIL,[user.email])
    
    return Response({
            "message": "If an account exists with this email, a password reset link will be sent."
        }, status=status.HTTP_200_OK)
    
class ResetPasswordAPIView(APIView):
  
  def post(self,request):
    email = request.data.get('email')
    user = User.objects.filter(email =email).first()
    if not user:
      return Response({'error': 'invalid reset request'},status=status.HTTP_400_BAD_REQUEST)
    serializer = ResetPasswordSerializer(user,data= request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
                {'message': 'Password reset successfully'},
                status=status.HTTP_200_OK
            )
    
    