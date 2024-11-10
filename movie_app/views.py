from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializer import (
    DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, MovieReviewSerializer, DirectorDetailSerializer)

@api_view(['GET', 'POST'])
def Directors_List(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')
        movies = request.data.get('movies')
        director = Director.objects.create(name=name)
        director.movies.set(movies)
        director.save()
        return Response(data=DirectorSerializer(instance=director, many=False).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def Director_Detail(request, pk):
    try:
        director = Director.objects.get(id=pk)
    except Director.DoesNotExist:
        return Response(data={"error": "Director not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorDetailSerializer(instance=director, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.movies.set(request.data.get('movies'))
        director.save()
        return Response(data=DirectorDetailSerializer(instance=director, many=False).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(data={"message": "Director deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def Movie_List(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        data = MovieSerializer(instance=movie, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director')
        director = Director.objects.get(id=director_id)
        movie = Movie.objects.create(title=title, description=description, duration=duration)
        movie.director = director
        movie.save()
        return Response(data=MovieDetailSerializer(instance=movie, many=False).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def Movie_Detail(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieDetailSerializer(instance=movie, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        director_id = request.data.get('director')
        director = Director.objects.get(id=director_id)
        movie.director = director
        movie.save()
        return Response(data=MovieDetailSerializer(instance=movie, many=False).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={"message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def Review_List(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(instance=review, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        movie_id = request.data.get('movie')
        movie = Movie.objects.get(id=movie_id)
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        review = Review.objects.create(movie=movie, rating=rating, comment=comment)
        return Response(data=ReviewSerializer(instance=review, many=False).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def Review_Detail(request, pk):
    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(instance=review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        movie_id = request.data.get('movie')
        movie = Movie.objects.get(id=movie_id)
        review.movie = movie
        review.rating = request.data.get('rating')
        review.comment = request.data.get('comment')
        review.save()
        return Response(data=ReviewSerializer(instance=review, many=False).data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(data={"message": "Review deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def Movies_Reviews(request):
    reviews = Review.objects.all()
    data = MovieReviewSerializer(instance=reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Review_By_Movie(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    review = Review.objects.filter(movie=movie)
    data = ReviewSerializer(instance=review, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)