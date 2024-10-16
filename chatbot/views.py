from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
import json
from django.db import connection


def window_view(request):
    if request.user.is_authenticated:
        return render(request, 'chatbot/chatting_page.html')
    else:
        return redirect(reverse("account:login"))

def answer_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        input_question = data.get("message")
        try:
            # 간단한 응답 (여기서 챗봇 로직 추가 가능)
            if input_question:
                # PostgreSQL 함수 호출
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM get_top_similar_questions('{input_question}');")
                    result = cursor.fetchone()  # 가장 유사한 질문 하나만 가져옴
            print(result)
            bot_reply = f"{result[0]}"
        except Exception as error:
            bot_reply = "다시 입력해 주세요!!!"
        return JsonResponse({"reply": bot_reply})