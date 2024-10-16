from django.urls import path, include
from recommend import views

app_name = "recommend"
urlpatterns = [
    path('movie/', views.movie_view, name='movie'),
    path('pop_movies/', views.load_movies, name='load_movies'),
    path('recom_customers/<str:model>/', views.load_customers, name='load_customers'),
]