from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.models import Permission, Group
import django.contrib.auth.password_validation as validators


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
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


class UserPermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class AuthGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True,
                                               queryset=Permission.objects.all(),
                                               slug_field="name")

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class UserGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        group_id = attrs.get("group_id")
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError({
                "user_id": "Not Exists"
            })
        group = Group.objects.filter(id=group_id).first()

        if not group:
            raise ValidationError({
                "group_id": "Not Exists"
            })
        if group in user.groups.all():
            raise ValidationError({
                "error": "User in group already"
            })
        return attrs


class UserSerializerForGroup(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            "id": {"read_only": True}
        }


class GroupDetailSerializer(serializers.ModelSerializer):
    """This Serializer is Used to List, Update and delete Group Details"""
    permissions = serializers.SlugRelatedField(many=True,
                                               queryset=Permission.objects.all(),
                                               slug_field="name")
    user_set = UserSerializerForGroup(many=True, read_only= True)
    """ Here user_set is Related name in Group and User mapping table so we can 
    fetch user by this Related name"""

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'user_set']
        extra_kwargs = {
            "id": {"read_only": True},
        }


class RemoveUserGroupSerializer(serializers.Serializer):
    """ This Serializer is Used To Remove User From Group """
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        group_id = attrs.get("group_id")
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError({
                "user_id": "Not Exists"
            })
        group = Group.objects.filter(id=group_id).first()

        if not group:
            raise ValidationError({
                "group_id": "Not Exists"
            })
        if group not in user.groups.all():
            print(user.groups.all())
            raise ValidationError({
                "error": "User is not in group "
            })
        return attrs
