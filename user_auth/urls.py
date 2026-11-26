from django.urls import path
from . import views

urlpatterns = [
  path('register/',views.UserRegistration.as_view()),
  path('login/',views.UserLogin.as_view()),
  path( 'forgot-password/',
        views.ForgotPasswordAPIView.as_view(),
        name='forgot-password'),
  path( 'reset-password/',
          views.ResetPasswordAPIView.as_view(),
          name='reset-password')
]