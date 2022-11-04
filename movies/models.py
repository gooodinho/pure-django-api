import uuid

from django.db import models


class PersonType(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Person(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.ManyToManyField(PersonType)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Movie(models.Model):
    MPA_RATING_CHOICES = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    poster = models.URLField()
    bg_picture = models.URLField()
    release_year = models.IntegerField()
    mpa_rating = models.CharField(max_length=50, choices=MPA_RATING_CHOICES)
    imdb_rating = models.FloatField()
    duration = models.IntegerField()
    persons = models.ManyToManyField(Person)
    genres = models.ManyToManyField(Genre)

    @property
    def directors(self):
        queryset = self.persons.filter(types__title__contains='director')
        return queryset

    @property
    def writers(self):
        queryset = self.persons.filter(types__title__contains='writer')
        return queryset

    @property
    def stars(self):
        queryset = self.persons.filter(types__title__contains='star')
        return queryset


    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-created_at']
