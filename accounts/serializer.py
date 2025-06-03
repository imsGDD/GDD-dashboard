# serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2'] # 'organizations',


#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({'Password': 'Password does not match'})
#         return attrs


#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             #organizations = validated_data['organizations'] 
#         )  
        
#         user.set_password(validated_data['password'])

#         user.save()
#         Token.objects.create(user=user)
#         return user
    
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         token = Token.objects.get(user=instance)
#         data['token'] = token.key
#         return data      

#############################################################################
from django.utils.translation import gettext as _



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2'] #'organizations', 


    def to_representation(self, instance):
        data = super().to_representation(instance)
        token = Token.objects.get(user=instance)
        data['token'] = token.key
        return data     
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields= ['email','password']




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
