import numpy as np
import json
from django.shortcuts import render, redirect, reverse
from recommend.dbCtrl import bring_dataframe_from_table
from recommend.models import Movies
from django.db.models import Case, When
from django.template.loader import render_to_string
from django.http import JsonResponse
from sklearn.metrics.pairwise import cosine_similarity


# Create your views here.
def movie_view(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'recommend/movies.html')
        return redirect(reverse("account:login"))
    except Exception as e:
        # 예외가 발생하면 로그를 남기고 오류 메시지를 반환
        print(f"Error in movie_view: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def load_movies(request):
    try:
        # popular_movies 데이터프레임 가져오기
        pop_movies = bring_dataframe_from_table('popular_movies', "postgres")

        # pop_movies에서 20개의 movie_id만 추출
        pop_movies_ids = pop_movies.sort_values('mean').iloc[:20, 1].to_list()

        # 결과 출력
        preserved_order = Case(*[When(movie_id=movie_id, then=pos) for pos, movie_id in enumerate(pop_movies_ids)])
        pop_movies_data = Movies.objects.filter(movie_id__in=pop_movies_ids).order_by(preserved_order)

        context = {
            "movies": pop_movies_data
        }
        movies_html = render_to_string("recommend/movies_list.html", context)
        return JsonResponse({'movies_html': movies_html})

    except Exception as e:
        # 예외 발생 시 오류 메시지와 함께 응답
        print(f"Error in load_movies: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
# Function to parse the string and convert to a list of floats
def parse_float_array(data):
    """JSON 형식의 문자열 배열을 float 배열로 변환"""
    if isinstance(data, str):
        data = json.loads(data)  # JSON 문자열을 배열로 변환
    return np.array(data, dtype=float)


# 코사인 유사도 계산

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
    """Postgres 테이블에서 모델에 따라 데이터프레임을 가져오는 함수"""
    return bring_dataframe_from_table(model_name, "postgres")

def get_recommend_movies(user_id, watched_movies, model_df, max_movies=20):
    """추천 영화를 필터링하여 최대 max_movies 개수만 반환"""
    remaining_movie_ids = []
    for movie_id in watched_movies:
        if not model_df[(model_df['user_id'] == user_id) & (model_df['movie_id'] == movie_id)].empty:
            movie_ids = recommend_movies(user_id, movie_id, model_df, 5.0, 200)
            remaining_movie_ids.extend(id for id in movie_ids if id not in watched_movies)
    return remaining_movie_ids[:max_movies]

def load_customers(request, model):
    try:
        user_id = request.user.user_id

        # 모델에 따라 데이터프레임 로드
        df = load_dataframe_from_model(model)

        # 사용자 고객 정보 로드
        customers = load_dataframe_from_model("customers")
        watched_movies = customers[customers['user_id'] == user_id]["movie_ids"].str.split(",").explode().astype(int).tolist()

        # LDA 모델일 경우 맞춤형 추천 알고리즘 사용
        if model == "lda_review_model":
            remaining_movie_ids = get_recommend_movies(user_id, watched_movies, df)
            print("no watched movies", remaining_movie_ids)
            if remaining_movie_ids == "No reviews":
                return JsonResponse({'customers_html': "<p>No movie reviews</p>"})
            if not remaining_movie_ids :
                return JsonResponse({'customers_html': "<p>No movie recommendations available</p>"})

        # 그 외 모델일 경우, 예측 평점을 기준으로 추천
        else:
            recommend_movie_ids = df[df["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
            recommend_movie_ids = recommend_movie_ids.iloc[:, 1].tolist()
            # print("recommend_movie_ids:", recommend_movie_ids)
            remaining_movie_ids = [movie_id for movie_id in recommend_movie_ids if movie_id not in watched_movies][:20]

        # print("not watched movies:", remaining_movie_ids)
        preserved_order = Case(*[When(movie_id=movie_id, then=pos) for pos, movie_id in enumerate(remaining_movie_ids)])
        recommend_movie_data = Movies.objects.filter(movie_id__in=remaining_movie_ids).order_by(preserved_order)

        if not recommend_movie_data.exists():
            return JsonResponse({'customers_html': "<p>No movie recommendations available</p>"})

        # 추천 영화 데이터 전달 및 렌더링
        context = {"customers": recommend_movie_data}
        customers_html = render_to_string("recommend/customers_list.html", context)
        return JsonResponse({'customers_html': customers_html})

    except Exception as e:
        print(f"Error in load_customers: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)