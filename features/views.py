from rest_framework import generics, status
from rest_framework.response import Response
from features.models import Tasklist, Task
from accounts.permissions import ModelPermission
from features.serializers import CreateTasklistSerializer, UpdateDeleteTasklistSerializer


class TasklistCreateAPIview(generics.CreateAPIView):
    queryset = Tasklist.objects.all()
    permission_classes = [ModelPermission]
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


class TasklistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasklist.objects.all()
    permission_classes = [ModelPermission]
    serializer_class = UpdateDeleteTasklistSerializer



