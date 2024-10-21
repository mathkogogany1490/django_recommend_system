# pca_app/views.py

import seaborn as sns
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from recommend.dbCtrl import bring_dataframe_from_table
from collections import Counter
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def genre_distribution_view(request):
    return render(request, 'chart/genre_distribution_view.html')


def pop_chart_view(request):
    pop_movies = bring_dataframe_from_table('popular_movies', "postgres")
    movies = bring_dataframe_from_table("movies", "postgres")
    # pop_movies에서 20개의 movie_id만 추출
    pop_movies_ids = pop_movies.sort_values('mean').iloc[:20, 1].to_list()
    filtered_movies = movies[movies['movie_id'].isin(pop_movies_ids)][['genre']]

    # 각 영화의 장르 문자열을 '|' 기준으로 분리한 후 하나의 리스트로 만듦
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()

    # 유니크한 장르값을 리스트로 변환
    all_genres = all_genres.tolist()

    # 주어진 리스트에서 각 장르의 앞뒤 공백을 제거한 후 개수를 셈
    cleaned_genres = [genre.strip() for genre in all_genres]
    genre_data = Counter(cleaned_genres)

    return JsonResponse(genre_data)


def histogram_data_view(request):
    # Load the iris dataset
    iris_data = sns.load_dataset('iris')

    # Extract features and labels
    X = iris_data[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
    y = iris_data["species"].values

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform PCA to reduce dimensions to 1 component
    pca = PCA(n_components=1)
    X_pca = pca.fit_transform(X_scaled)

    # Add the reduced PCA component to the original dataset
    iris_data['PCA1'] = X_pca

    # Prepare PCA data for each species
    pca_hist_data = {
        'setosa': iris_data[iris_data['species'] == 'setosa']['PCA1'].tolist(),
        'versicolor': iris_data[iris_data['species'] == 'versicolor']['PCA1'].tolist(),
        'virginica': iris_data[iris_data['species'] == 'virginica']['PCA1'].tolist()
    }

    return JsonResponse(pca_hist_data)