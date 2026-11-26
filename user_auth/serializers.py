from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'phone_number',
            'first_name',
            'last_name'
        ]
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
      
      
class ForgotPasswordSerializer(serializers.Serializer):
  email = serializers.EmailField()
  

class ResetPasswordSerializer(serializers.Serializer):
  
  token = serializers.CharField()
  new_password = serializers.CharField(min_length = 8,write_only = True)
  confirm_password = serializers.CharField(min_length = 8,write_only = True)
    
  def validate(self, attrs):
    if attrs['new_password'] != attrs['confirm_password']:
      raise serializers.ValidationError("Password doesn't match.")
    user = self.instance
    if not default_token_generator.check_token(user,attrs['token']):
      raise serializers.ValidationError({'error': 'invalid or expired token.'})
      
    return attrs
  
  def update(self,instance,validated_data):
    instance.set_password(validated_data['new_password'])
    instance.save()
    return instance