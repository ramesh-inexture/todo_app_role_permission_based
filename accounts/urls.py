from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (AuthUserRegistrationView, AllPermissionListAPIView, GroupListCreateAPIView,
                    AssignRoleCreateAPIView, GroupRetriveAPIview, GroupManageAPIView, RemoveGroupUserAPIView)

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthUserRegistrationView.as_view(), name='user_registration'),
    path('list_all_permissions/', AllPermissionListAPIView.as_view(), name='assign_user_role'),
    path('create_group/', GroupListCreateAPIView.as_view(), name='create_group'),
    path('assign_role/', AssignRoleCreateAPIView.as_view(), name='assign_role'),
    path('see_group_detail/<int:pk>/', GroupRetriveAPIview.as_view(), name='group_detail'),
    path('manage_group_detail/<int:pk>/', GroupManageAPIView.as_view(), name='manage_group_detail'),
    path('manage_group_user/<int:pk>/<int:uk>/', RemoveGroupUserAPIView.as_view(), name='manage_group_user'),
]
