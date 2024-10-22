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
def cust_chart_view(request):
    user_id = request.user.user_id
    # print(type(user_id))
    customers = bring_dataframe_from_table('customers', "postgres")
    movies = bring_dataframe_from_table("movies", "postgres")
    # 특정 user_id를 가진 고객의 영화 장르 정보를 가져옴
    user_movie_ids = customers[customers['user_id'] == user_id]['movie_ids'].apply(
        lambda x: [int(movie_id) for movie_id in x.split(',')]  # 쉼표로 나눈 후 숫자(int)로 변환
    )
    # print("****", user_genres)
    user_genre_list = user_movie_ids.explode().tolist()  # 장르 데이터를 리스트로 변환
    # print("*****", user_genre_list[:10])
    filtered_movies = movies[movies['movie_id'].isin(user_genre_list)]
    # print(filtered_movies)
    # 각 영화의 장르를 '|' 또는 ',' 기준으로 분리한 후 하나의 리스트로 만듦
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()

    # 결과 확인용 출력
    print(all_genres)

    # 유니크한 장르값을 리스트로 변환
    all_genres = all_genres.tolist()

    # 주어진 리스트에서 각 장르의 앞뒤 공백을 제거한 후 개수를 셈
    cleaned_genres = [genre.strip() for genre in all_genres]
    genre_data = Counter(cleaned_genres)

    return JsonResponse(genre_data)
def svd_chart_view(request):
    user_id = request.user.user_id
    svd_matrix = bring_dataframe_from_table("svd_model", "postgres")
    svd_movie_ids = svd_matrix[svd_matrix["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
    svd_movie_ids = svd_movie_ids.iloc[:100, 1].to_list()
    # print(svd_movie_ids)
    movies = bring_dataframe_from_table("movies", "postgres")
    # pop_movies에서 20개의 movie_id만 추출
    filtered_movies = movies[movies['movie_id'].isin(svd_movie_ids)][['genre']]

    # 각 영화의 장르 문자열을 '|' 기준으로 분리한 후 하나의 리스트로 만듦
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()

    # 유니크한 장르값을 리스트로 변환
    all_genres = all_genres.tolist()

    # 주어진 리스트에서 각 장르의 앞뒤 공백을 제거한 후 개수를 셈
    cleaned_genres = [genre.strip() for genre in all_genres]
    genre_data = Counter(cleaned_genres)

    return JsonResponse(genre_data)
def nmf_chart_view(request):
    user_id = request.user.user_id
    nmf_matrix = bring_dataframe_from_table("nmf_model", "postgres")
    nmf_movie_ids = nmf_matrix[nmf_matrix["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
    nmf_movie_ids = nmf_movie_ids.iloc[:100, 1].to_list()
    # print(svd_movie_ids)
    movies = bring_dataframe_from_table("movies", "postgres")
    # pop_movies에서 20개의 movie_id만 추출
    filtered_movies = movies[movies['movie_id'].isin(nmf_movie_ids)][['genre']]

    # 각 영화의 장르 문자열을 '|' 기준으로 분리한 후 하나의 리스트로 만듦
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()

    # 유니크한 장르값을 리스트로 변환
    all_genres = all_genres.tolist()

    # 주어진 리스트에서 각 장르의 앞뒤 공백을 제거한 후 개수를 셈
    cleaned_genres = [genre.strip() for genre in all_genres]
    genre_data = Counter(cleaned_genres)

    return JsonResponse(genre_data)
def mf_chart_view(request):
    user_id = request.user.user_id
    mf_matrix = bring_dataframe_from_table("mf_model", "postgres")
    mf_movie_ids = mf_matrix[mf_matrix["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
    mf_movie_ids = mf_movie_ids.iloc[:100, 1].to_list()
    # print(svd_movie_ids)
    movies = bring_dataframe_from_table("movies", "postgres")
    # pop_movies에서 20개의 movie_id만 추출
    filtered_movies = movies[movies['movie_id'].isin(mf_movie_ids)][['genre']]

    # 각 영화의 장르 문자열을 '|' 기준으로 분리한 후 하나의 리스트로 만듦
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()

    # 유니크한 장르값을 리스트로 변환
    all_genres = all_genres.tolist()

    # 주어진 리스트에서 각 장르의 앞뒤 공백을 제거한 후 개수를 셈
    cleaned_genres = [genre.strip() for genre in all_genres]
    genre_data = Counter(cleaned_genres)

    return JsonResponse(genre_data)