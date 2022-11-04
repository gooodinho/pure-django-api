from django.contrib import admin
from .models import PersonType, Person, Genre, Movie

admin.site.register(PersonType)
admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Movie)
