from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import SeptaUserListCreateView, SeptaUserDetailView

urlpatterns = [
    # gets all user profiles and create a new profile
    path(
        "all-septa-users",
        SeptaUserListCreateView.as_view(),
        name="all-septa-users"
    ),
    # retrieves profile details of the currently logged in user
    path(
        "septa-user/<int:pk>",
        SeptaUserDetailView.as_view(),
        name="septa-user"),
]
