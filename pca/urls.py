from django.urls import path
from pca import views

app_name = "pca"
urlpatterns = [
    path('pca_view/', views.scatter_plot_view, name='pca_view'),
    path('scatter/', views.pca_view, name='scatter'),
    path('histogram/', views.histogram_data_view, name='histogram'),
]