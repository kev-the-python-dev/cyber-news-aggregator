from django.urls import path
from news.views import reddit_scrape, list_news, article_scrape

urlpatterns = [
    path('scrape/', article_scrape, name="scrape"),
    path('scrape_reddit/', reddit_scrape, name="scrape_reddit"),
    path('',list_news, name="home"),
]
