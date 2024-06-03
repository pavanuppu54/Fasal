from django.urls import reverse
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import MovieList, Movie
from .forms import MovieListForm
from django.contrib.auth.decorators import login_required

def home(request):
    movies = fetch_omdb_movies("action", 20)  # Fetch 20 movies with the search term "action"
    movie_lists = MovieList.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'movies/home.html', {'movie_lists': movie_lists, 'movies': movies})

def search_movies(request):
    movie_lists = MovieList.objects.filter(user=request.user) if request.user.is_authenticated else []
    movies = []
    if request.method == "POST":
        query = request.POST.get('query')
        movies = fetch_omdb_movies(query)
    return render(request, 'movies/search.html', {'movies': movies, 'movie_lists': movie_lists})

@login_required
def create_list(request):
    if request.method == "POST":
        form = MovieListForm(request.POST)
        if form.is_valid():
            movie_list = form.save(commit=False)
            movie_list.user = request.user
            movie_list.save()
            return redirect('home')
    else:
        form = MovieListForm()
    return render(request, 'movies/create_list.html', {'form': form})

@login_required
def add_movie_to_list(request, list_id, imdb_id):
    movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
    response = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}")
    data = response.json()
    movie, created = Movie.objects.get_or_create(movie_list=movie_list, title=data['Title'], imdb_id=imdb_id)
    if created:
        movie.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_movie_to_list_home(request, imdb_id):
    if request.method == "POST":
        list_id = request.POST.get('list_id')
        movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
        response = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}")
        data = response.json()
        movie, created = Movie.objects.get_or_create(movie_list=movie_list, title=data['Title'], imdb_id=imdb_id)
        if created:
            movie.save()
        messages.success(request, f"Added {data['Title']} to {movie_list.name}")
    return redirect('home')

@login_required
def view_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
    movies = movie_list.movies.all()
    for movie in movies:
        response = requests.get(f"http://www.omdbapi.com/?i={movie.imdb_id}&apikey={settings.OMDB_API_KEY}")
        data = response.json()
        movie.poster = data.get('Poster', '')
        movie.year = data.get('Year', '')
        movie.runtime = data.get('Runtime', '')
    return render(request, 'movies/view_list.html', {'movie_list': movie_list, 'movies': movies})

def fetch_omdb_movies(query, limit=None):
    movies = []
    response = requests.get(f"http://www.omdbapi.com/?s={query}&apikey={settings.OMDB_API_KEY}")
    data = response.json()
    if limit:
        movies += data.get('Search', [])[:limit]
    else:
        movies += data.get('Search', [])
    for movie in movies:
        response = requests.get(f"http://www.omdbapi.com/?i={movie['imdbID']}&apikey={settings.OMDB_API_KEY}")
        details = response.json()
        movie['poster'] = details.get('Poster', '')
        movie['year'] = details.get('Year', '')
        movie['runtime'] = details.get('Runtime', '')
    return movies
