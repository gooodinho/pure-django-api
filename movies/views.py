import math

from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Genre, Movie


ITEMS_PER_PAGE = 2


def genres(request) -> JsonResponse:
    try:
        genres = Genre.objects.all()
        data = list(genres.values('id', 'title'))
        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({"error": ["internal"]})


def movie_info(request, movie_id: int) -> JsonResponse:
    try:
        try:
            movie = get_object_or_404(Movie, id=movie_id)
        except Http404:
            return JsonResponse({"error": ["movie__not_found"]})
        data = {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year,
            "mpa_rating": movie.mpa_rating,
            "imdb_rating": movie.imdb_rating,
            "duration": movie.duration,
            "poster": movie.poster,
            "bg_picture": movie.bg_picture,
            "genres": list(movie.genres.values('id', 'title')),
            "directors": list(movie.directors.values('id', 'first_name', 'last_name')),
            "writers": list(movie.writers.values('id', 'first_name', 'last_name')),
            "stars": list(movie.stars.values('id', 'first_name', 'last_name'))
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": ["internal"]})


def movie_list(request) -> JsonResponse:
    try:
        genre_id = request.GET.get('genre', None)
        src = request.GET.get('src', None)
        page = request.GET.get('page', None)
        movies = Movie.objects.all()
        if genre_id:
            try:
                genre = get_object_or_404(Genre, id=genre_id)
                movies = movies.filter(genres__id=genre.id)
            except Http404:
                return JsonResponse({"error": ["genre__invalid"]})
        if src:
            if len(src) < 2 or len(src) > 20:
                return JsonResponse({"error": ["src__invalid"]})
            movies = movies.filter(title__icontains=src)

        if page:
            try:
                page = int(page)
                offset = ITEMS_PER_PAGE*page
                limit = ITEMS_PER_PAGE*page+ITEMS_PER_PAGE
                movies_quantity = movies.count()
                if limit > movies_quantity > offset:
                    movies = movies[offset:]
                elif offset > movies_quantity:
                    return JsonResponse({"error": ["page__out_of_bounds"]})
                else:
                    movies = movies[offset:limit]
            except Exception:
                return JsonResponse({"error": ["page__invalid"]})
        
        final_movies_quantity = movies.count()
        data = {
            "total": final_movies_quantity,
            "pages": math.ceil(final_movies_quantity / ITEMS_PER_PAGE),
            "results": []
        }

        for movie in movies:
            movie_data = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_year": movie.release_year,
                "mpa_rating": movie.mpa_rating,
                "imdb_rating": movie.imdb_rating,
                "duration": movie.duration,
                "poster": movie.poster,
                "bg_picture": movie.bg_picture,
                "genres": list(movie.genres.values('id', 'title')),
                "directors": list(movie.directors.values('id', 'first_name', 'last_name')),
                "writers": list(movie.writers.values('id', 'first_name', 'last_name')),
                "stars": list(movie.stars.values('id', 'first_name', 'last_name'))
            }
            data['results'].append(movie_data)

        return JsonResponse(data)
    except Exception as e:
        # print(e)
        return JsonResponse({"error": ["internal"]})