import pandas as pd
from django.shortcuts import render, redirect, reverse
from recommend.dbCtrl import bring_dataframe_from_table
from recommend.models import Movies
from django.db.models import Case, When
from django.template.loader import render_to_string
from django.http import JsonResponse


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


def load_customers(request, model):
    try:
        user_id = request.user.user_id
        df = pd.DataFrame()

        # 모델에 따라 데이터프레임 가져오기
        if model == "svd_model":
            df = bring_dataframe_from_table(model, "postgres")
        elif model == "nmf_model":
            df = bring_dataframe_from_table(model, "postgres")
        elif model == "mf_model":
            df = bring_dataframe_from_table(model, "postgres")

        customers = bring_dataframe_from_table("customers", "postgres")

        # 현재 사용자가 본 영화 목록 추출
        movie_ids_watched = customers[customers['user_id'] == user_id]["movie_ids"].str.split(",").explode().astype(
            int).tolist()

        # 예측 모델에서 추천된 영화 목록을 추출
        recommend_movie_ids = df[df["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
        recommend_movie_ids = recommend_movie_ids.iloc[:100, 1].to_list()

        # 이미 본 영화를 제외하고 나머지 영화 ID 추출
        remaining_movie_ids = [movie_id for movie_id in recommend_movie_ids if movie_id not in movie_ids_watched]
        remaining_movie_ids = remaining_movie_ids[:20]

        # remaining_movie_ids가 비어 있는지 확인
        if not remaining_movie_ids:
            print("No remaining movie IDs to recommend.")
            return JsonResponse({'customers_html': "<p>No movie recommendations available</p>"})

        # Case를 사용하여 영화 순서를 보존한 채로 정렬
        preserved_order = Case(*[When(movie_id=movie_id, then=pos) for pos, movie_id in enumerate(remaining_movie_ids)])
        recommend_movie_data = Movies.objects.filter(movie_id__in=remaining_movie_ids).order_by(preserved_order)

        print (remaining_movie_ids)
        # 추천된 영화가 있는지 확인
        if not recommend_movie_data.exists():
            print(f"No movies found for IDs: {remaining_movie_ids}")
            return JsonResponse({'customers_html': "<p>No movie recommendations available</p>"})

        # 템플릿에 추천된 영화 데이터를 전달
        context = {
            "customers": recommend_movie_data
        }

        # 추천된 영화 목록을 템플릿으로 렌더링
        customers_html = render_to_string("recommend/customers_list.html", context)
        return JsonResponse({'customers_html': customers_html})

    except Exception as e:
        # 예외 발생 시 오류 메시지와 함께 응답
        print(f"Error in load_customers: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
