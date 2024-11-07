from django.db import models
from django.db.models import Count

class Director(models.Model):
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField('Movie', related_name='directors', blank=True)

    @property
    def movie_count(self):
        return self.movies.count()
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


RATING = ((rating, '* ' * rating) for rating in range(1, 6))


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING, default=1)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.comment