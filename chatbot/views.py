from django.shortcuts import render, redirect, reverse
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
import json
import requests
import numpy as np
from recommend.dbCtrl import *
from django.db import connection
from bs4 import BeautifulSoup
from recommend.models import Movies


def get_top_movies():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=박스오피스'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # ul 태그 선택
    ul = soup.select_one(
        '#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div.mflick > div._panel_popular._tab_content > div.list_image_info.type_pure_top > div > ul:nth-child(1)')
    lis = ul.find_all('li')

    # 영화 제목 리스트 초기화
    pop_movies = []
    for idx, li in enumerate(lis):
        # 영화 제목 추출
        title = li.select_one('.title').text.strip() if li.select_one('.title') else li.text.strip()
        pop_movies.append(title)

        # 다섯 개까지만 추출
        if idx == 4:
            break

    return pop_movies

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
    """Postgres 테이블에서 모델에 따라 데이터프레임을 가져오는 함수"""
    return bring_dataframe_from_table(model_name, "postgres")
def get_recommend_movies(user_id, watched_movies, model_df):
    """추천 영화를 필터링하여 최대 max_movies 개수만 반환"""
    remaining_movie_ids = []
    for movie_id in watched_movies:
        if not model_df[(model_df['user_id'] == user_id) & (model_df['movie_id'] == movie_id)].empty:
            movie_ids = recommend_movies(user_id, movie_id, model_df, 5.0, 200)
            remaining_movie_ids.extend(id for id in movie_ids if id not in watched_movies)
    return remaining_movie_ids
def whole_recomm_movies(request, model):
    try:
        user_id = request.user.user_id

        # 모델에 따라 데이터프레임 로드
        df = load_dataframe_from_model(model)

        # 사용자 고객 정보 로드
        customers = load_dataframe_from_model("customers")
        watched_movies = customers[customers['user_id'] == user_id]["movie_ids"].str.split(",").explode().astype(int).tolist()
        # print(watched_movies)
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
            remaining_movie_ids = [movie_id for movie_id in recommend_movie_ids if movie_id not in watched_movies]

        return remaining_movie_ids

    except Exception as e:
        print(f"No reccommeded movies")
        return;

def each_genre_recomm(request, model, genre):
    movie_ids = whole_recomm_movies(request, model)
    # movie_ids에 해당하고 Action 장르인 영화의 제목 리스트 저장
    action_titles = list(
        Movies.objects.filter(id__in=movie_ids, genre__icontains=genre).values_list("title", flat=True)
    )
    return action_titles

def window_view(request):
    if request.user.is_authenticated:
        return render(request, 'chatbot/chatting_page.html')
    else:
        return redirect(reverse("account:login"))

def answer_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        input_question = data.get("message")
        # print(input_question)
        try:
            # 간단한 응답 (여기서 챗봇 로직 추가 가능)
            if input_question:
                # PostgreSQL 함수 호출
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM get_top_similar_questions('{input_question}');")
                    result = cursor.fetchone()  # 가장 유사한 질문 하나만 가져옴
            if result[1] == '개봉작':
                top_movies = get_top_movies()
                answer = result[0].replace("[]", ', '.join(top_movies))
            elif result[1] == "액션":
                recomm_movies = each_genre_recomm(request, "svd_model", "Action")
                recomm_movies = [m for idx,  m in enumerate(recomm_movies) if idx < 3]
                answer = result[0].replace("[]", ', '.join(recomm_movies))
            bot_reply = answer


        except Exception as error:
            bot_reply = "다시 입력해 주세요!!!"
        return JsonResponse({"reply": bot_reply})