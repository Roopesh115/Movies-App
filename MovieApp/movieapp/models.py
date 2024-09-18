from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    year = models.PositiveIntegerField()
    img = models.ImageField(upload_to='movies/')
    actors = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='movies')
    trailer = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Ensure this returns a string
        return f"{self.movie.name} - {self.rating}/5"