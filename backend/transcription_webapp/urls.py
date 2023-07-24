from django.urls import path, include
from rest_framework import routers

from .views import FileView

router = routers.DefaultRouter()

router.register('files', FileView)

urlpatterns = [
    path(r'', include(router.urls)),
]