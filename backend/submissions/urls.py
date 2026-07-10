from django.urls import path
from .views import SubmitSolutionView, SubmissionHistoryView

urlpatterns = [
    path('submit/', SubmitSolutionView.as_view(), name='submit-solution'),
    path("history/<str:room_code>/",  SubmissionHistoryView.as_view(), name="submission-history"),
    path("<int:submission_id>/", SubmissionDetailView.as_view(), name="submission-detail")
]