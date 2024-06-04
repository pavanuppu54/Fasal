from django.db import models
from django.contrib.auth.models import User

# Existing models in app/models.py

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_list = models.ForeignKey(MovieList, related_name="movies", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title
