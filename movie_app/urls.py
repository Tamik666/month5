from django.urls import path
from . import views

urlpatterns = [ 
    path('directors/', views.DirectorList.as_view()),
    path('directors/<int:pk>/', views.DirectorDetail.as_view()),
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('movies/reviews/', views.MovieList.as_view),
    path('movies/<int:pk>/reviews/', views.ReviewByMovieView.as_view),
        ]