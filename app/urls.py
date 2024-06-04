from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('feedback/', views.feedback, name='feedback'),
    path('search/', views.search_movies, name='search_movies'),
    path('create-list/', views.create_list, name='create_list'),
    path('add-movie/<int:list_id>/<str:imdb_id>/', views.add_movie_to_list, name='add_movie_to_list'),
    path('add-movie-home/<str:imdb_id>/', views.add_movie_to_list_home, name='add_movie_to_list_home'),
    path('view-list/<int:list_id>/', views.view_list, name='view_list'),
    

]
