from django.contrib import admin
from recommend.models import Movies
# Register your models here.

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'genre', 'movie_image')
    search_fields = ['movie_id']
    list_filter = ['title']