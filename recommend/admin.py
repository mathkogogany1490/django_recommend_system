from django.contrib import admin
from recommend.models import Movies
# Register your models here.

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'genres', 'movie_image')