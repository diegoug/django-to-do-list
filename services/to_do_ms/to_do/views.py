from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Task

from .serializers import TaskModelSerializer

class TaskViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    
    authentication_classes = [OAuth2Authentication]
    
    search_fields = ['description']
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
