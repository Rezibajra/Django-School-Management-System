from django.urls import path

from .views import ResultListView, create_result, edit_results, ResultClassListView

urlpatterns = [
    path("create/", create_result, name="create-result"),
    path("edit-results/", edit_results, name="edit-results"),
    path("view/all", ResultListView.as_view(), name="view-results"),
    path("view/<int:pk>", ResultClassListView.as_view(), name="student-class-resp"),
]
