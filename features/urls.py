from django.urls import path
from features.views import TasklistCreateAPIview, TasklistRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('create_tasklist/', TasklistCreateAPIview.as_view(), name='create_tasklist'),
    path('manage_tasklist/<int:pk>/', TasklistRetrieveUpdateDestroyAPIView.as_view(), name='manage_tasklist'),
]
