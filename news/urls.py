from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_feed, name='news_feed'),
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),
]
