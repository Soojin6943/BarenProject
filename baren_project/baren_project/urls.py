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

from django.contrib import admin
from django.urls import path, include
# TokenObtainRairView = 액세스 및 리프레시 토큰 발급
# TokenRefreshView = 리프레시 토큰으로 새로운 액세스 토큰 발급
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # JWT 기반 로그인/회원가입
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # news_app 관련 url은 news/ 로 통일
    path('news/', include('news_app.urls')),
]
