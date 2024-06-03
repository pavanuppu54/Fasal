from django.contrib import admin
from django.urls import path, include
from movies import views as movie_views

urlpatterns = [
    path('', movie_views.home, name='home'),
    path('search/', movie_views.search_movies, name='search_movies'),
    path('create_list/', movie_views.create_list, name='create_list'),
    path('list/<int:list_id>/add/<str:imdb_id>/', movie_views.add_movie_to_list, name='add_movie_to_list'),
    path('list/<int:list_id>/', movie_views.view_list, name='view_list'),
    path('add_movie_to_list_home/<str:imdb_id>/', movie_views.add_movie_to_list_home, name='add_movie_to_list_home'),  # Add this line
]
