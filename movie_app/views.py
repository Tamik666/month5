from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializer import (
    DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, MovieReviewSerializer, DirectorDetailSerializer,
    MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer)

@api_view(['GET', 'POST'])
def Directors_List(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serilizer = DirectorValidateSerializer(data=request.data)
        if not serilizer.is_valid():
            return Response(data=serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = serilizer.validated_data.get('name')
        movies = serilizer.validated_data.get('movies')
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
        serilizer = DirectorValidateSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        director.name = serilizer.validated_data.get('name')
        director.movies.set(serilizer.validated_data.get('movies'))
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
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
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
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
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
        serailizer = ReviewValidateSerializer(data=request.data)
        if not serailizer.is_valid():
            return Response(data=serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
        movie_id = serailizer.validated_data.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        rating = serailizer.validated_data.get('rating')
        comment = serailizer.validated_data.get('comment')
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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.validated_data.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        review.movie = movie
        review.rating = serializer.validated_data.get('rating')
        review.comment = serializer.validated_data.get('comment')
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