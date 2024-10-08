from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import *


class UserSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'data', 'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверный учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'phone_number', 'data']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class MovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['movie_name']


class DirectorListSerializer(serializers.ModelSerializer):
    movies = MovieSimpleSerializer()

    class Meta:
        model = Director
        fields = ['director_name', 'director_image', 'movies']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name', 'actor_image']


class GenerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gener
        fields = ['gener_name']


class RatingSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    movies = MovieSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['user', 'movies', 'stars', ]



class MovieLanguagesSerializer(serializers.ModelSerializer):
    # movie=MovieSimpleSerializer()
    class Meta:
        model = MovieLanguages
        fields = ['movie_languages','video']


class MovieListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%d-%m-%Y')
    ratings = RatingSimpleSerializer(many=True, read_only=True)
    country = CountrySerializer(read_only=True)
    languages=MovieLanguagesSerializer(many=True,read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'date', 'country', 'ratings', 'average_rating',
                  'movie_time', 'movie_image', 'movie_status','languages' ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    director = DirectorListSerializer(many=True, read_only=True)
    actor = ActorListSerializer(many=True, read_only=True)
    gener = GenerListSerializer(many=True, read_only=True)
    ratings = RatingSimpleSerializer(many=True, read_only=True)
    date = serializers.DateTimeField(format='%d-%m-%Y')
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'date', 'country', 'director', 'actor', 'gener', 'ratings',
                  'average_rating',
                  'movie_time', 'description', 'movie_trailer', 'movie_image', 'movie_status', 'quality', ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    movies = MovieSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['user', 'movies', 'stars', 'parent', 'text', 'created_date']


class DirectorSerializer(serializers.ModelSerializer):
    movies = MovieSimpleSerializer()

    class Meta:
        model = Director
        fields = ['director_name', 'age', 'bio', 'director_image', 'movies']


class ActorSerializer(serializers.ModelSerializer):
    movies = MovieSimpleSerializer()

    class Meta:
        model = Actor
        fields = ['actor_name', 'age', 'actor_image', 'bio', 'movies']


class GenerSerializer(serializers.ModelSerializer):
    movies = MovieSimpleSerializer()

    class Meta:
        model = Gener
        fields = ['gener_name', 'movies']


class FavoriteSerializer(serializers.ModelSerializer):
    created_data = serializers.DateTimeField(format='%d-%m-%Y')
    users = UserProfileSimpleSerializer()

    class Meta:
        model = Favorite
        fields = ['users', 'created_data']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    cart = FavoriteSerializer()
    movies = MovieSimpleSerializer(read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ['cart', 'movies']


class HistorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    movies = MovieSimpleSerializer()
    viewed_at = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = History
        fields = ['user', 'movies', 'viewed_at']


class MomentsSerializer(serializers.ModelSerializer):
    movies = MovieSimpleSerializer()

    class Meta:
        model = Moments
        fields = ['movie_moment', 'movies']


