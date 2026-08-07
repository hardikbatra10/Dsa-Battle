from django.urls import path
from .views import CreateRoomView, JoinRoomView, RoomDetailView, StartRoomView, EndRoomView, LeaveRoomView, LeaderboardView, MyRoomsView

urlpatterns = [
    path("create/", CreateRoomView.as_view(), name = 'create-room'),
    path("join/", JoinRoomView.as_view(), name = 'join-room'),
    path("mine/", MyRoomsView.as_view(), name = 'my-rooms'),
    path('<str:room_code>/', RoomDetailView.as_view(), name='room-detail'),
    path('<str:room_code>/start/', StartRoomView.as_view(), name='start-room'),
    path("<str:room_code>/end/", EndRoomView.as_view(), name="end-room"),
    path("<str:room_code>/leave/", LeaveRoomView.as_view(), name="leave-room"),
    path("<str:room_code>/leaderboard/", LeaderboardView.as_view(), name="room-leaderboard"),
]

