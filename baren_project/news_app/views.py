from django.shortcuts import render
from dotenv import load_dotenv
from django.http import JsonResponse

# 네이버 api 호출 파트
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Create your views here.

# 네이버 api 호출------------------------------------------

# 네이버 api 키 가져오기 (.env 파일에 있음)
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

# 네이버 api 함수
def search_naver_news(query):
    '''
    
    '''
    # 기본 요청 url (뒤에 헤더랑 필요 요청 매개변수 붙어야함)
    url = "https://openapi.naver.com/v1/search/news.json"
    # 헤더
    headers = {
        "X-NAVER-Client-Id": NAVER_CLIENT_ID,
        "X-NAVER-Client-Secret": NAVER_CLIENT_SECRET,
    }
    # 파라미터
    params = {
        "query": query,
        "display": 10, # 검색 결고 개수
        "start": 1, # 검색 시작 위치
        "sort": "sim" # 정렬 방식 (sim = 유사도순, date = 날짜순, -붙이면 내림차순인가 오름차순으로 변경)
    }
    
    # 최종 키워드 검색 요청 url
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []
    
    


# 검색창 관련 함수 (검색값 입력 및 결과 리턴)
def search_news(request):
    query = request.GET.get('query', '')
    
    # 쿼리 있으면 search_naver_news 함수에 쿼리 보내고 템플릿은 search_results.html
    if query:
        news_list = search_naver_news(query)
        return render(request, 'news/search_results.html', {'news_list':news_list})
    else:
        '''
        TODO : 검색 결과 오류 화면 처리(팝업..)
        '''
        return render(request, 'news/search_form.html')
