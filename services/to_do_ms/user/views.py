from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from profiles.models import User

from .serializers import UserModelSerializer, UserUpdateModelSerializer, UserLoginSerializer, UserSignUpSerializer

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, 
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    
    authentication_classes = [OAuth2Authentication]
    
    search_fields = ['email', 'first_name', 'last_name']
    filter_backends = [filters.SearchFilter]

    lookup_field = 'email'
    lookup_value_regex = '[\w.@+-]+'
    
    # custom actions ----------------------------------------------------------
    def get_permissions(self):
        if 'post' in self.action_map:
            if self.action_map['post'] in ['signup', 'login']:
                return []
        return super(UserViewSet, self).get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'update':
            return UserUpdateModelSerializer
        return super(UserViewSet, self).get_serializer_class()

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, client_secret, client_id = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'client_secret': client_secret,
            'client_id': client_id
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)