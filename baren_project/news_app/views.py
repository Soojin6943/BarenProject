from django.shortcuts import render
from dotenv import load_dotenv
from django.http import JsonResponse

# 네이버 api 호출 파트
import os
import requests
from dotenv import load_dotenv

# 본문 크롤링 파트
from bs4 import BeautifulSoup
import pandas as pd
import time # 크롤링 딜레이를 위한 모듈

load_dotenv()

# Create your views here.

# 본문 크롤링 ---------------------------------------------
# 개별 뉴스 url에서 본문을 크롤링하는 함수
def crawl_news_content(url):
    # Args: 
    #     url (str): 크롤링할 뉴스 기사의 url
    # Returns:
    #     str or None: 성공 시 뉴스 본문 텍스트, 실패시 None
    
    try:
        # 차단 방지를 위한 브라우저 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        
        # HTTP GET 요청 보내기
        response = requests.get(url, headers=headers)
        
        # 응답 상태 코드 확인
        if response.status_code != 200:
            print(f"HTTP 요청 실패: {response.status_code}")
            return None
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 뉴스인 경우의 처리
        if 'news.naver.com' in url:
            # 네이버 뉴스 본문 영역 선택자
            content = soup.select_one('#dic_area')
            if content:
                # HTML 태그 제거하고 순수 텍스트만 추출
                return content.get_text().strip()
            else:
                print(f"본문 영역을 찾을 수 없습니다: {url}")

        # TODO : 다른 언론사 사이트 추가
        # elif 'other_news_site.con' in url : 
        #    content = soup.select_one('다른 선택자')
        
        return None
    
    except Exception as e:
        print(f"크롤링 중 오류 발생: {url}")
        print(f"오류 내용: {str(e)}")
        return None
 
 
# 검색 결과 데이터프레임의 모든 기사에 대해 본문을 크롤링하여 추가하는 함수   
def crawl_news_data(search_results_df, delay=1):
    # 본문 저장할 새로운 컬럼
    search_results_df['content'] = None
    
    # 전체 크롤링 진행상황 표시용 변수
    total = len(search_results_df)
    
    for idx, row in search_results_df.iterrows():
        # 현재 진행 상황 출력
        print(f"크롤링 진행중...({idx+1}/{total})")
        
        url = row['news_url']
        
        # 네이버 뉴스 URL인 경우만 크롤링
        if url and 'news.naver.com' in url:  
        
            # 본문 크롤링 수행
            content = crawl_news_content(url)
        
            if content:
                # 크롤링 성공 시 데이터프레임에 저장
                search_results_df.at[idx, 'content'] = content
                print(f"성공: {row['title']}")
            else:
                print(f"실패: {row['title']}")
        else:
            print(f"네이버 뉴스 링크 아님: {row['title']}")
        
        # 과도한 요청 방지를 위한 대기
        time.sleep(delay)
        
    return search_results_df
    
    
    

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
        # TODO : 검색 결과 개수 조정하기 현재는 구현 단계기 때문에 10개만 받아오게 함
        
        "query": query,
        "display": 10, # 검색 결과 개수
        "start": 1, # 검색 시작 위치
        "sort": "sim" # 정렬 방식 (sim = 유사도순, date = 날짜순, -붙이면 내림차순인가 오름차순으로 변경)
    }
    
    # 최종 키워드 검색 요청 url
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        # API 응답을 DataFrame으로 변환
        items = response.json().get('items', [])
        df = pd.DataFrame(items)
        
        # 네이버 뉴스 링크 추출
        def extract_naver_link(row):
            try:
                if 'originallink' in row and 'link' in row:
                    # 네이버 뉴스 링크가 있으면 그것을 사용
                    if 'news.naver.com' in row['link']:
                        return row['link']
                    # 없으면 originallink 사용
                    return row['originallink']
            except:
                return None
            
        # 새로운 컬럼에 네이버 뉴스 링크 저장
        df['news_url'] = df.apply(extract_naver_link, axis=1)
        return df
    else:
        return pd.DataFrame() # 빈 DataFrame 반환
    
    
#-----------------------------------------------------------

# 검색창 관련 함수 (검색값 입력 및 결과 리턴)
def search_news(request):
    query = request.GET.get('query', '')
    
    # 쿼리 있으면 search_naver_news 함수에 쿼리 보내고 템플릿은 search_results.html
    if query:
        # 네이버 검색 api 결과를 DataFame으로 받기
        search_results_df = search_naver_news(query)
        
        # DataFrame이 비어있지 않은 경우만 크롤링 실행
        if not search_results_df.empty:
            # 본문 크롤링
            results_with_content = crawl_news_data(search_results_df)
            
            # DataFrame을 템플릿에서 사용할 수 있는 형태로 변환
            news_list = results_with_content.to_dict('records')
            return render(request, 'news/search_results.html', {'news_list': news_list})
        
        
    return render(request, 'news/search_form.html')