from django.urls import path
from . import views

urlpatterns = [ 
    path('directors/', views.Directors_List),
    path('directors/<int:pk>/', views.Director_Detail),
    path('movies/', views.Movie_List),
    path('movies/<int:pk>/', views.Movie_Detail),
    path('reviews/', views.Review_List),
    path('reviews/<int:pk>/', views.Review_Detail),
    path('movies/reviews/', views.Movies_Reviews),
    path('movies/<int:pk>/reviews/', views.Review_By_Movie),
        ]