from django.urls import path
from news.views import article_scrape, list_news

urlpatterns = [
    path('scrape/', article_scrape, name="scrape"),
    path('',list_news, name="home"),
]
