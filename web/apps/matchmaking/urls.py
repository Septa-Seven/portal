from django.urls import path

from apps.matchmaking import views


urlpatterns = [
    path('games/<int:pk>/', views.GamesRetrieveView.as_view()),
    path('games/', views.GamesListView.as_view()),
    path('leagues/<int:pk>/', views.LeagueRetrieveView.as_view()),
    path('leagues/', views.LeagueListView.as_view()),
    path('leagues/<int:pk>/top/', views.LeagueTopView.as_view()),
]
