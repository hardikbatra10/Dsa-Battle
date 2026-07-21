from django.urls import path
from .views import SubmitSolutionView, RunSolutionView, SubmissionHistoryView, SubmissionDetailView

urlpatterns = [
    path('submit/', SubmitSolutionView.as_view(), name='submit-solution'),
    path('run/', RunSolutionView.as_view(), name='run-solution'),
    path("history/<str:room_code>/",  SubmissionHistoryView.as_view(), name="submission-history"),
    path("<int:submission_id>/", SubmissionDetailView.as_view(), name="submission-detail")
]