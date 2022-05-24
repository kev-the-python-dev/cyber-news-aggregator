import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as beautsoup
from news.models import Headline

def article_scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent" : "Googlebot/2.1; +https://www.google.com/bot.html)"}
    url = "https://www.thehackernews.com"

    content = session.get(url, verify=False).content
    soup = beautsoup(content, "html.parser")
    news = soup.find_all('div', {"class":"body-post"})

    
    for news_item in news:
        main = news_item.find_all('a')[0]
        link = main['href']
        img_src = str(main.find('img')['data-src'])
        title_main = news_item.find('h2')
        title = str(title_main.text)

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = img_src
        new_headline.save()
    
    return redirect('../')


def list_news(request):
    headlines = Headline.objects.all()[::1]
    context = {
        "object_list" : headlines

    }
    return render(request, "news/home.html", context)
