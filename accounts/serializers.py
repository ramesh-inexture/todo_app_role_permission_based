from rest_framework import serializers
from accounts.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'user_name',
            'password',
            'password2'

        )
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate_password(self, data):
        validators.validate_password(password=data)
        return data

    """ validating password and confirm password """

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user
