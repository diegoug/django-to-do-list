from django.contrib.auth import password_validation, authenticate

from oauth2_provider.models import Application

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class UserUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('The credentials are not valid')

        self.context['user'] = user
        return data

    def create(self, data):
        oauth_data = {
            'user': self.context['user'],
            'authorization_grant_type': 'password'
        }

        if not Application.objects.filter(**oauth_data).exists():
            oauth_application = Application(**oauth_data)
            oauth_application.save()

        oauth2_app = Application.objects.get(**oauth_data)

        return self.context['user'], oauth2_app.client_secret, oauth2_app.client_id


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    first_name = serializers.CharField(
        min_length=2, max_length=50)
    last_name = serializers.CharField(
        min_length=2, max_length=100)

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        min_length=8, max_length=64)
    password_confirmation = serializers.CharField(
        min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Passwords do not match')
        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user
