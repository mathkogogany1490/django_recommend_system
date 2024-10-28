from django.db import models

# Create your models here.
class Movies(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=1000)
    movie_image = models.ImageField("영화 이미지", upload_to="recommend/thumbnails", blank=True, null=True)
