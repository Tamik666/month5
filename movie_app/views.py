from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializer import (
    DirectorSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, MovieReviewSerializer, DirectorDetailSerializer)

@api_view(['GET'])
def Directors_List(request):
    directors = Director.objects.all()
    data = DirectorSerializer(instance=directors, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Director_Detail(request, pk):
    try:
        director = Director.objects.get(id=pk)
    except Director.DoesNotExist:
        return Response(data={"error": "Director not found"}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorDetailSerializer(instance=director, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def Movie_List(request):
    movie = Movie.objects.all()
    data = MovieSerializer(instance=movie, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def Movie_Detail(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    data = MovieDetailSerializer(instance=movie, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def Review_List(request):
    review = Review.objects.all()
    data = ReviewSerializer(instance=review, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def Review_Detail(request, pk):
    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response(data={"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(instance=review, many=False).data
    return Response(data=data, status=status.HTTP_200_OK)


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