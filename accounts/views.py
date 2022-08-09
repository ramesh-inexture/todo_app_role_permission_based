from django.contrib.auth.models import Permission, Group
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from .permissions import ModelPermission
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import User
from accounts.serializers import UserRegistrationSerializer, UserPermissionsSerializer, \
    AuthGroupSerializer, UserGroupSerializer, GroupDetailSerializer, RemoveUserGroupSerializer, UserProfileSerializer


class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


def get_user_permissions(user):
    if user.is_superuser:
        # print(Permission.objects.all())
        return Permission.objects.all()
    print("------*********************************************------------------------------------")
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


class GroupListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [ModelPermission]
    serializer_class = AuthGroupSerializer
    queryset = Group.objects.all()


class AllPermissionListAPIView(generics.ListAPIView):
    permission_classes = [ModelPermission]
    Serializer_class = UserPermissionsSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = self.request.user
        obj = get_user_permissions(user)
        return obj

    def list(self, request, *args, **kwargs):
        obj = self.get_object().order_by('id')
        serializer = UserPermissionsSerializer(instance=obj, many=True)
        return Response(serializer.data)


class AssignRoleCreateAPIView(APIView):
    permission_classes = [ModelPermission]
    queryset = Group.objects.none()

    def post(self, request):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get('user_id')
            group_id = serializer.data.get('group_id')
            user_obj = User.objects.get(id=user_id)
            group_obj = Group.objects.get(id=group_id)
            user_obj.groups.add(group_obj)
            obj = user_obj.groups.all()
            return Response(
                {'success': True,
                 'message': 'User successfully Assigned To the Group!'},
                status=status.HTTP_200_OK)

        return Response({"details": "Some Error is Occurred"}, status=status.HTTP_400_BAD_REQUEST)


class GroupRetriveAPIview(generics.ListAPIView):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, ModelPermission]

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group_queryset = Group.objects.filter(id=pk)
        self.check_object_permissions(self, self.request.user)
        return group_queryset

    def get(self, request, pk):

        # user = User.objects.get(id=request.user.id)
        # if user.has_perms()
        # print(type(request.user))

        user = request.user
        print(request.method)
        queryset = self.get_queryset().first()
        serializer = GroupDetailSerializer(instance=queryset)
        return Response(
            {
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )


class GroupManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [ModelPermission]
    serializer_class = GroupDetailSerializer

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group_queryset = Group.objects.filter(id=pk)
        self.check_object_permissions(self, self.request.user)
        return group_queryset

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return Response(
            {
                "message": "Successfully Updated",
                "data": response.data
            },
            response.status_code)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        return Response(
            {
                "message": "Successfully Deleted",
                "data": response.data
            },
            response.status_code)


class RemoveGroupUserAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, uk, *args, **Kwargs):
        print(pk, uk)
        data = {
            "user_id": uk,
            "group_id": pk
        }
        serializer = RemoveUserGroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get('user_id')
            group_id = serializer.data.get('group_id')
            user_obj = User.objects.get(id=user_id)
            group_obj = Group.objects.get(id=group_id)
            user_obj.groups.remove(group_obj)
            # obj = user_obj.groups.all()
            return Response(
                {'success': True,
                 'message': 'User successfully Removed From Group!'},
                status=status.HTTP_204_NO_CONTENT)

        return Response({"details": "Some Error is Occurred"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    permission_classes = [ModelPermission]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()



