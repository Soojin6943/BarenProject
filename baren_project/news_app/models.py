from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

# 기사 관련 테이블
class Article(models.Model):
    # PK 지정 및 자동 증가 
    article_id = models.AutoField(primary_key=True)
    # 기사 제목 (최대 255자)
    title = models.CharField(max_length=255)
    # 기사 본문 
    content = models.TextField()
    # 기사 원본 URL (unique=True로 중복 url 저장 방지/ URLField로 url 유효성 검사)
    url = models.URLField(unique=True)
    # 기사 발행 날짜 및 시간
    published_date = models.DateTimeField()
    # 낚시성 점수
    clickbait_score = models.IntegerField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ]
    )
    # 분석 요약 (예: "낚시성 표현 발견", "과장된 제목")
    analysis_summary = models.TextField(null=True, blank=True)
    # 관련 태그
    tags = models.CharField(max_length=255, null=True, blank=True)
    # db 생성 시간 (자동으로 현재 시간 저장)
    created_at = models.DateTimeField(default=timezone.now)
    
    # 객체 출력 시 제목 나타나게
    def __str__(self):
        return self.title
    
    # def search_by_tag(tag):
    #     return Article.objects.filter(tags__icontains=tag)
    
    class Meta:
        # 테이블 이름 지정 (선택사항)
        db_table = 'articles'
        # 정렬 순서 지정 (최신 기사가 먼저 나오도록)
        ordering = ['-published_date']
        
class UserNewsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # 중복 즐겨찾기 방지

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
