from django import forms
from .models import MovieList

class MovieListForm(forms.ModelForm):
    class Meta:
        model = MovieList
        fields = ['name', 'is_public']  # Assuming 'name' and 'is_public' are fields in your MovieList model
