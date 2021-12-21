
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

router = DefaultRouter()
router.register(r'task', TaskViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls))
]
