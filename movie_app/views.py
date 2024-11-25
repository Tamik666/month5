from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Director, Movie, Review
from .serializer import (
    DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, MovieReviewSerializer, DirectorDetailSerializer,
    MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer)
class DirectorList(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        movies = serializer.validated_data.get('movies')
        director = Director.objects.create(name=name)
        if movies is not None:
            director.movies.set(movies)
        director.save()
        return Response(data=self.get_serializer(instance=director, many=False).data, status=status.HTTP_201_CREATED)


class DirectorDetail(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Director deleted"}, status=status.HTTP_204_NO_CONTENT)


class MovieList(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieValidateSerializer

    def perform_create(self, serializer):
        try:
            director = Director.objects.get(id=serializer.validated_data.get('director_id'))
        except Director.DoesNotExist:
            raise serializer.ValidationError({"error": "Director not found"})
        serializer.save(director=director)

class MovieDetail(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieValidateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            director = Director.objects.get(id=serializer.validated_data.get('director_id'))
        except Director.DoesNotExist:
            raise serializers.ValidationError({"error": "Director not found"})
        serializer.save(director=director)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT)

class ReviewList(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewValidateSerializer

    def perform_create(self, serializer):
        try:
            movie = Movie.objects.get(id=serializer.validated_data.get('movie_id'))
        except Movie.DoesNotExist:
            raise serializer.ValidationError({"error": "Movie not found"})
        serializer.save(movie=movie)


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewValidateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            movie = Movie.objects.get(id=serializer.validated_data.get('movie_id'))
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"error": "Movie not found"})
        serializer.save(movie=movie)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Review deleted"}, status=status.HTTP_204_NO_CONTENT)


class MoviesReviewsView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = MovieReviewSerializer



class ReviewByMovieView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        movie_id = self.kwargs.get('pk')
        try:
            movie = Movie.objects.get(id=movie_id)
            return Review.objects.filter(movie=movie)
        except Movie.DoesNotExist:
            return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
