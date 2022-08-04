from django.urls import path, include
from .views import (
    HelloWorld,
)

urlpatterns = [
    path('api', HelloWorld.as_view()),
]