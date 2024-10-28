# pca_app/views.py

import numpy as np
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from recommend.dbCtrl import bring_dataframe_from_table

def genre_distribution_view(request):
    if request.user.is_authenticated:
        return render(request, 'chart/genre_distribution_view.html')
    return redirect(reverse("account:login"))

# 공통 유틸리티 함수들
def parse_float_array(data):
    """JSON 형식의 문자열 배열을 float 배열로 변환"""
    if isinstance(data, str):
        data = json.loads(data)  # JSON 문자열을 배열로 변환
    return np.array(data, dtype=float)


def find_similar_movies(user_id, movie_id, df, top_n=10):
    """특정 영화와 유사한 영화를 찾기 위한 함수"""
    movie_vector = df[(df['user_id'] == user_id) & (df['movie_id'] == movie_id)]['topic_vector'].values[0]
    movie_vector = parse_float_array(movie_vector)

    # 모든 topic_vector를 float 배열로 변환
    df['topic_vector'] = df['topic_vector'].apply(parse_float_array)

    similarities = cosine_similarity([movie_vector], list(df['topic_vector'].values))
    df['similarity'] = similarities[0]

    return df.sort_values(by='similarity', ascending=False).head(top_n)

def recommend_movies(user_id, movie_id, df, rating_threshold=4.5, top_n=10):
    """추천 영화를 필터링하여 반환"""
    similar_movies = find_similar_movies(user_id, movie_id, df, top_n=top_n)
    recommended_movies = similar_movies[similar_movies['rating'] >= rating_threshold]
    return recommended_movies['movie_id']

def load_dataframe_from_model(model_name):
    """모델에 따라 Postgres에서 데이터프레임 로드"""
    return bring_dataframe_from_table(model_name, "postgres")

def get_genre_data(movie_ids, movies_df):
    """주어진 movie_id 목록에 해당하는 장르 데이터를 집계"""
    filtered_movies = movies_df[movies_df['movie_id'].isin(movie_ids)][['genre']]
    all_genres = filtered_movies['genre'].apply(lambda x: x.split(',')).explode()
    cleaned_genres = [genre.strip() for genre in all_genres.tolist()]
    return Counter(cleaned_genres)

def get_recommend_movies(user_id, watched_movies, model_df, max_movies=20):
    """추천 영화를 필터링하여 최대 max_movies 개수만 반환"""
    remaining_movie_ids = []
    for movie_id in watched_movies:
        if not model_df[(model_df['user_id'] == user_id) & (model_df['movie_id'] == movie_id)].empty:
            movie_ids = recommend_movies(user_id, movie_id, model_df, 5.0, 200)
            remaining_movie_ids.extend(id for id in movie_ids if id not in watched_movies)
    return remaining_movie_ids[:max_movies]

# Chart View Functions
def pop_chart_view(request):
    try:
        pop_movies = bring_dataframe_from_table('popular_movies', "postgres")
        movies = bring_dataframe_from_table("recommend_movies", "postgres")
        pop_movie_ids = pop_movies.sort_values('mean').iloc[:20, 1].tolist()
        genre_data = get_genre_data(pop_movie_ids, movies)
        return JsonResponse(genre_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def cust_chart_view(request):
    try:
        user_id = request.user.user_id
        customers = bring_dataframe_from_table('customers', "postgres")
        movies = bring_dataframe_from_table("recommend_movies", "postgres")
        user_movie_ids = customers[customers['user_id'] == user_id]['movie_ids'].apply(lambda x: [int(id) for id in x.split(',')]).explode().tolist()
        genre_data = get_genre_data(user_movie_ids, movies)
        return JsonResponse(genre_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def svd_chart_view(request):
    return generate_model_chart_view(request, "svd_model")

def nmf_chart_view(request):
    return generate_model_chart_view(request, "nmf_model")

def mf_chart_view(request):
    return generate_model_chart_view(request, "mf_model")


def lda_chart_view(request):
    try:
        user_id = request.user.user_id
        df = load_dataframe_from_model("lda_review_model")
        df['topic_vector'] = df['topic_vector'].apply(parse_float_array)  # topic_vector를 float 배열로 변환
        customers = load_dataframe_from_model("customers")
        watched_movies = customers[customers['user_id'] == user_id]["movie_ids"].str.split(",").explode().astype(
            int).tolist()

        # remaining_movie_ids가 없으면 빈 응답을 반환
        remaining_movie_ids = get_recommend_movies(user_id, watched_movies, df)
        if not remaining_movie_ids:
            return JsonResponse({'error': 'No recommended movies available.'}, status=200)

        # 장르 데이터가 없으면 빈 응답 반환
        movies = bring_dataframe_from_table("recommend_movies", "postgres")
        genre_data = get_genre_data(remaining_movie_ids, movies)
        if not genre_data:
            return JsonResponse({'error': 'No genre data available.'}, status=200)

        return JsonResponse(genre_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 공통 로직을 포함한 모델 기반 차트 뷰 생성 함수
def generate_model_chart_view(request, model_name):
    try:
        user_id = request.user.user_id
        model_matrix = bring_dataframe_from_table(model_name, "postgres")
        top_movie_ids = model_matrix[model_matrix["user_id"] == user_id].sort_values("predicted_rating", ascending=False).iloc[:100, 1].tolist()
        movies = bring_dataframe_from_table("recommend_movies", "postgres")
        genre_data = get_genre_data(top_movie_ids, movies)
        return JsonResponse(genre_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
