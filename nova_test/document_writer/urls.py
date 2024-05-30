from django.urls import path
from .views import CreateFileView

urlpatterns = [
    path('create-file/', CreateFileView.as_view(), name='create-file'),
]
