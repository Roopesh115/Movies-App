from django.urls import path
from . import views

app_name = 'movieapp'

urlpatterns = [
    # Home page displaying list of movies
    path('', views.index, name='index'),

    # Movie detail page
    path('movie/<int:movie_id>/', views.detail, name='detail'),

    # Add a new movie
    path('add/', views.add_movie, name='add_movie'),

    # Update an existing movie
    path('update/<int:movie_id>/', views.update, name='update'),

    # Delete a movie
    path('delete/<int:movie_id>/', views.delete, name='delete'),

    # Add review (if handled separately in the future)
    # path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
]
