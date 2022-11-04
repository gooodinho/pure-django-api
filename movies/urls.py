from django.urls import path
from .views import genres, movie_info, movie_list


urlpatterns = [
    path('api/v1/genres/', genres, name='genres'),
    path('api/v1/movies/', movie_list, name='movie_list'),
    path('api/v1/movies/<int:movie_id>/', movie_info, name="movie info"),
]