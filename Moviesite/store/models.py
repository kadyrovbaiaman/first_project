from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18),
                                                       MaxValueValidator(100)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    data=models.DateField(auto_now_add=True,null=True,blank=True)
    STATUS_CHOICES = (
        ('pro', 'pro'),
        ('simple', 'simple')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='simple', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18),
                                                       MaxValueValidator(100)])
    director_image = models.ImageField(upload_to='director_image/', null=True, blank=True)

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18),
                                                       MaxValueValidator(100)])
    actor_image = models.ImageField(upload_to='actor_image/', null=True, blank=True)

    def __str__(self):
        return self.actor_name


class Gener(models.Model):
    gener_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.gener_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='movies', on_delete=models.CASCADE)
    director = models.ManyToManyField(Director, related_name='movies')
    actor = models.ManyToManyField(Actor, related_name='movies',
                                   verbose_name='Movie Actors and Actress')
    gener = models.ManyToManyField(Gener, related_name='movies')
    movie_time = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='About the Movie')
    movie_trailer = models.FileField(upload_to='movie_video/', verbose_name='Trailer', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_image/', verbose_name='image', null=True, blank=True)

    # movie MovieLanguages
    STATUS_MOVIE = (
        ('pro', 'pro'),
        ('simple', 'simple')
    )
    movie_status = models.CharField(max_length=50, choices=STATUS_MOVIE, default='simple', null=True, blank=True)
    # types(144, 360, 480, 720, 1080)
    CHOICES_QUALITY = (
        ('144', '144p'),
        ('360', '360p'),
        ('480', '480p'),
        ('720', '720p'),
        ('1080', '1080p')
    )
    quality= MultiSelectField(choices=CHOICES_QUALITY)


    def __str__(self):
        return f'{self.movie_name}'

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class MovieLanguages(models.Model):
    movie_languages = models.CharField(max_length=50, null=True, blank=True)
    video = models.FileField(upload_to='languages_video/', null=True, blank=True)
    movie = models.ForeignKey(Movie, related_name='languages', on_delete=models.CASCADE)


class Moments(models.Model):
    movies = models.ForeignKey(Movie, related_name='moments', on_delete=models.CASCADE)
    movie_moment = models.ImageField(upload_to='moment_image/', null=True, blank=True)


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], verbose_name='rating',
                                null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user}-{self.movies}-{self.stars}'


class Favorite(models.Model):
    users = models.OneToOneField(UserProfile, related_name='favorites', on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.users}'


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
