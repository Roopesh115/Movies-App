from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .form import ReviewForm, MovieForm
from .models import Movie, Review, Category

# Display a list of movies with optional search and category filter
def index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        movies = Movie.objects.filter(name__icontains=query)  # Ensure 'name' is the correct field
    else:
        movies = Movie.objects.all()

    if category_id:
        movies = movies.filter(categories__id=category_id)  # Correct related field for filtering

    categories = Category.objects.all()
    return render(request, 'index.html', {'movielist': movies, 'categories': categories, 'query': query})


# Display detailed information about a specific movie
def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()  # Get all reviews related to the movie
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movieapp:detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews, 'form': form})

# Add a new movie
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('movieapp:index')
    else:
        form = MovieForm()

    categories = Category.objects.all()  # Fetch all available categories
    return render(request, 'add.html', {'form': form, 'categories': categories})

# Update an existing movie
def update(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.user != movie.added_by:
        return HttpResponseForbidden("You are not allowed to edit this movie.")

    form = MovieForm(request.POST or None, request.FILES or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('movieapp:index')

    return render(request, 'edit.html', {'form': form, 'movie': movie})

# Delete an existing movie
def delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.user != movie.added_by:
        return HttpResponseForbidden("You are not allowed to delete this movie.")

    if request.method == "POST":
        movie.delete()
        return redirect('movieapp:index')

    return render(request, 'delete.html', {'movie': movie})
