from django.urls import path
from .views import CreateRoomView, JoinRoomView, RoomDetailView

urlpatterns = [
    path("create/", CreateRoomView.as_view(), name = 'create-room'),
    path("join/", JoinRoomView.as_view(), name = 'join-room'),
    path('<str:room_code>/', RoomDetailView.as_view(), name='room-detail')
]
