"""
URL configuration for Afisha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', views.Directors_List),
    path('api/v1/directors/<int:pk>/', views.Director_Detail),
    path('api/v1/movies/', views.Movie_List),
    path('api/v1/movies/<int:pk>/', views.Movie_Detail),
    path('api/v1/reviews/', views.Review_List),
    path('api/v1/reviews/<int:pk>/', views.Review_Detail),
    path('api/v1/movies/reviews/', views.Movies_Reviews),
    path('api/v1/movies/<int:pk>/reviews/', views.Review_By_Movie),
]

