from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name movie_count'.split()


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name movies movie_count'.split()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title director'.split()
        depth = 1

class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, max_length=1000)
    director_id = serializers.CharField(max_length=100)
    duration = serializers.IntegerField(default=0, required=False)

    def validate_director_id(self, director_id):
        if not director_id:
            raise serializers.ValidationError("Director id is required")
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise serializers.ValidationError("Director not found")
        return director_id



class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    movies = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_movies(self, movies):
        existing_movies = Movie.objects.filter(id__in=movies)
        if len(existing_movies) != len(movies):
            raise ValidationError('Movies does not exist')
        return movies
    

class ReviewValidateSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, max_length=1000)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.CharField(min_length=1)

    def validate_movie_id(self, movie_id):
        if not movie_id:
            raise serializers.ValidationError("Movie id is required")
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie not found")
        return movie_id