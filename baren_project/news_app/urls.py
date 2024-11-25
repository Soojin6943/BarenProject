"""
URL configuration for baren_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views




urlpatterns = [

    # 로그인 페이지
    path('login/', views.login_page, name='login_page'),
    # 로그아웃 페이지
    path('logout/', views.logout_page, name='logout_page'),
    
    # 회원가입
    path("signup/", views.signup_view, name='signup'),
    
    # 로그인 성공 시 리디렉션
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # news/search/ - 이건 views의 search_news로 보내짐/ 뉴스 검색 페이지
    path("search/", views.search_news, name='search_news'),

    

]
