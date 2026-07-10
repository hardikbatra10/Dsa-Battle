from django.urls import path
from .views import CreateRoomView, JoinRoomView, RoomDetailView, StartRoomView, EndRoomView

urlpatterns = [
    path("create/", CreateRoomView.as_view(), name = 'create-room'),
    path("join/", JoinRoomView.as_view(), name = 'join-room'),
    path('<str:room_code>/', RoomDetailView.as_view(), name='room-detail'),
    path('<str:room_code>/start/', StartRoomView.as_view(), name='start-room'),
    path("<str:room_code>/end/", EndRoomView.as_view(), name="end-room")
]

