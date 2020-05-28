from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.login, name='login'),
    path('pdm1', views.pdm1, name='pdm1'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('update_scores', views.update_scores, name='update_scores'),
    path('forming', views.forming, name='forming'),
    path('create_match', views.create_match, name='create_match'),
    path('constraints', views.constraints, name='constraints'),
    path('select_team', views.select_team, name='select_team'),
    path('Home', views.Home, name='Home'),
    path('PlayerDashboard', views.PlayerDashboard, name='PlayerDashboard'),
    path('Leaderboard', views.Leaderboard, name='Leaderboard'),
    path('CreateTeam', views.CreateTeam, name='CreateTeam'),
    path('Profile', views.Profile, name='Profile'),
    path('Players_list', views.Players_list, name='Players_list'),
    path('get_points', views.get_points, name='get_points'),
    path('user_team', views.user_team, name='user_team'),
    path('leaderboardeval', views.leaderboardeval, name='leaderboardeval'),
    path('add_players', views.add_players, name='add_players'),
]