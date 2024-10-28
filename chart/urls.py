from django.urls import path
from chart import views

app_name = "chart"
urlpatterns = [
    path('genre_view/', views.genre_distribution_view, name='genre_chart'),
    path('pop_genre_chart/', views.pop_chart_view, name='pop_chart'),
    path('cust_genre_chart/', views.cust_chart_view, name='cust_chart'),
    path('svd_genre_chart/', views.svd_chart_view, name='svd_chart'),
    path('nmf_genre_chart/', views.nmf_chart_view, name='nmf_chart'),
    path('mf_genre_chart/', views.mf_chart_view, name='mf_chart'),
    path('lda_genre_chart/', views.lda_chart_view, name='lda_review_chart'),
]