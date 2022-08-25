from django.urls import path
from features.views import TasklistCreateAPIview, TasklistRetrieveUpdateDestroyAPIView, TaskCreateAPIView, \
    TaskRetrieveUpdateDestroyAPIView, SearchTaskView, NotificationsView, SubtaskCreateAPIView, TaskRetrieveAPIView, \
    TasklistRetrieveAPIView

urlpatterns = [
    path('create_tasklist/', TasklistCreateAPIview.as_view(), name='create_tasklist'),
    path('manage_tasklist/<int:pk>/', TasklistRetrieveUpdateDestroyAPIView.as_view(), name='manage_tasklist'),
    path('create_task/', TaskCreateAPIView.as_view(), name='create_task'),
    path('create_subtask/', SubtaskCreateAPIView.as_view(), name='create_subtask'),
    path('manage_task/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='manage_task'),
    path('search_task/', SearchTaskView.as_view(), name='search_task'),
    path('notification/', NotificationsView.as_view(), name='notification'),
    path('task_detail/<int:pk>/', TaskRetrieveAPIView.as_view(), name='task_detail'),
    path('tasklist_detail/<int:pk>/', TasklistRetrieveAPIView.as_view(), name='tasklist_detail'),
]
