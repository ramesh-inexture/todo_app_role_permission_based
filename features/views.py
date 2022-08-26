from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from features.models import Tasklist, Task, Notification
from accounts.permissions import ModelPermission, IsOwner, IsOwnerOrModelPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from features.serializers import CreateTasklistSerializer, UpdateDeleteTasklistSerializer, CreateTaskSerializer, \
    ManageTaskSerializer, SearchTaskSerializer, NotificationSerializer, CreateSubtaskSerializer, SubtaskModelSerializer, \
    RetrieveTasklistSerializer, TaskRetrieveSerializer


class TasklistCreateAPIview(generics.CreateAPIView):
    """This class handles creation of tasklist in Tasklist Model,
    Here ModelPermission allows only permitted user to Create Tasklist
    """
    queryset = Tasklist.objects.all()
    # permission_classes = [ModelPermission]
    serializer_class = CreateTasklistSerializer

    def post(self, request, *args, **kwargs):
        created_by = request.user.id
        data = request.data.copy()
        data['created_by'] = created_by
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                "status": "success",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class TasklistRetrieveUpdateDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """This class handles Retrieve,Update and Destroy of tasklist in Tasklist Model,
    Here ModelPermission allows only permitted user to Manage Tasklist
    """
    queryset = Tasklist.objects.all()
    permission_classes = [IsOwnerOrModelPermission]
    serializer_class = UpdateDeleteTasklistSerializer

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return Response({
            'message': "Successfully Updated",
            'data': response.data,
            'status': response.status_code
        })

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        return Response({
            'data': response.data,
            'status': response.status_code
        })


class TaskCreateAPIView(generics.CreateAPIView):
    """This Class is used to create task in Task Model,
    Here we have to provide list (tasklist_id), title, desc to create Task
    """
    queryset = Task.objects.all()
    permission_classes = [ModelPermission]
    serializer_class = CreateTaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                "status": "success",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """This class Contains Apis for Retrieve, Update and Destroy of task from Task Model
     here permission_classes Contain Permission for if he had ModelPermission or IsOwner"""

    serializer_class = ManageTaskSerializer
    queryset = Task.objects.all()
    permission_classes = [ModelPermission]

    def get_object(self):
        pk = self.kwargs['pk']
        task_obj = get_object_or_404(Task, id=pk)
        self.check_object_permissions(self.request, task_obj.list.created_by)
        return task_obj

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


class SubtaskCreateAPIView(generics.CreateAPIView):
    """This Class is used to create Subtask in Task Model and also add them in Subtask Model,
    Here we have to provide task (task_id of parent task), and list (tasklist_id), title, desc to create SubTask
    """

    queryset = Task.objects.all()
    serializer_class = CreateSubtaskSerializer
    permission_classes = [ModelPermission]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'task' in data:
            task = data['task']
            task_obj = Task.objects.get(id=task)
            list = task_obj.list.id
        else:
            raise ValidationError({"task": "required_field"})
        data['list'] = list
        data['is_subtask'] = True
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            subtask_data = serializer.data
            id = serializer.data['id']
            data['sub_task'] = id
            serializer = SubtaskModelSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    "status": "success",
                    "subtask_data": subtask_data
                }
                return Response(response, status=status.HTTP_201_CREATED)


class SearchTaskView(generics.ListAPIView):
    """ Search Friend Through This APIView, We can Search Task by Providing task's title """
    permission_classes = [IsAuthenticated]
    """ Getting Serializer to Show Data When User Searches Their Task """
    serializer_class = SearchTaskSerializer
    queryset = Task.objects.all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user.id
        queryset = Task.objects.filter(list__created_by=user)
        return queryset


class NotificationsView(generics.ListAPIView):
    """This class is used to get all notification from notification table"""
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(receiver=self.request.user)
        return queryset


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """This View is used to retrieve Task Details"""
    serializer_class = TaskRetrieveSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrModelPermission]

    def get_object(self):
        pk = self.kwargs['pk']
        # Use objects.filter().first() don't use objects.get() bcz it may occur error if data not found
        obj = Task.objects.filter(id=pk).first()
        if not obj:
            raise ValidationError({"Error": "No Data Found"})
        self.check_object_permissions(self.request, obj.list.created_by)
        return obj


class TasklistRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveTasklistSerializer
    queryset = Tasklist.objects.all()
    permission_classes = [IsOwnerOrModelPermission]

    def get_object(self):
        pk = self.kwargs['pk']
        obj = Tasklist.objects.filter(id=pk).first()
        if not obj:
            raise ValidationError({"Error": "No Data Found"})
        self.check_object_permissions(self.request, obj.created_by)
        return obj