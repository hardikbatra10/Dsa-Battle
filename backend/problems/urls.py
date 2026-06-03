from django.urls import path
from .views import CreateProblemView, ListProblemView

urlpatterns = [
    path("create/", CreateProblemView.as_view(), name='create-problem'),
    path("", ListProblemView.as_view(), name='list-problems'),
]
