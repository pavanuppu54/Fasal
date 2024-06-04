from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from project import settings
from .tokens import generate_token
from .models import MovieList, Movie
import requests
from .forms import MovieListForm  

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be 20 characters or fewer!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "ᗰOᐯIEᔕᑎOᗯ @ Confirm your Email"
        email_message = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.send()

        messages.success(request, "Your account has been created! Please check your email to confirm your email address.")
        return redirect('signin')

    return render(request, "authentication/signup.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        # Sending feedback via email
        email_subject = f"New Feedback from {name}"
        email_message = f"Name: {name}\nEmail: {email}\nRating: {rating}\n\nMessage:\n{message}"

        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_FEEDBACK_RECIPIENT],
        )

        messages.success(request, "Thank you for your feedback!")
        return redirect('home')
    return render(request, 'movies/home.html')

def home(request):
    movies = fetch_omdb_movies("action", 20)
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
