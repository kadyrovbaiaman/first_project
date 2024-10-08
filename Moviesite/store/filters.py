from django_filters import FilterSet
from .models import Movie, Rating


class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'country': ['exact'],
            'date': ['gt', 'lt'],
            'gener': ['exact'],
            'movie_status': ['exact'],
            'actor': ['exact'],
            'director': ['exact'],

        }


class RatingFilter(FilterSet):
    class Meta:
        model = Rating
        fields = {
            'stars': ['gt', 'lt']
        }
