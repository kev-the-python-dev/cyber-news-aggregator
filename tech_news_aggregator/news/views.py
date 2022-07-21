from news.models import Headline
from datetime import datetime
from django.db import IntegrityError
import praw, requests

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as beautsoup # Scrapy is better for this, as we can crawl multiple sites


def reddit_scrape(request):
    # Unlike the below function, we will be using Reddit API (PRAW) to pull posts
    user_agent = 'User-Agent: #'
    reddit = praw.Reddit(client_id='#', client_secret='#', user_agent=user_agent)

    # Pre-reqs
    top_posts = reddit.subreddit('Python').top(limit=6)
    
    # Scraping execution
    try:
        for top_post in top_posts:
            title = top_post.title
            
            # Make date human readable
            publish_date = datetime.utcfromtimestamp(top_post.created)
            pub_year = publish_date.year
            pub_month = publish_date.month
            pub_day = publish_date.day

            link = top_post.permalink
            img_src = 'https://i.guim.co.uk/img/media/02c5fc2b42591243e6292fc83f8a97ed78807b57/198_0_2000_1200/master/2000.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=d31d7a8f045e54151b84076280aebca8'
            
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = 'https://www.reddit.com/' + link
            new_headline.image = img_src
            new_headline.date = f'{pub_day}/{pub_month}/{pub_year}'

            try:
                new_headline.save()
            except Exception as e:
                print(e)
    except IntegrityError:
        print('Duplicate reddit posts found. Ommitting and moving forward.')
    finally:
        return redirect('../')

def article_scrape(request): # This is specifically for TheHackerNews.com. 
    # For additional websites, create additional functions that mirror this function's 'function' although BS4 selector changes will be needed.
    session = requests.Session() # Session object performs far better due to cookie persistance and re-useable TCP connections 
    session.headers = {"User-Agent" : "Googlebot/2.1; +https://www.google.com/bot.html)"} # Using Googlebot will allow us to freely scrape without being blocked.
    url = "https://www.thehackernews.com" # If you change this, you'll need to re-do all the selectors BeautifulSoup parses.

    # Establishing the response, creating the HTML parser (since identifying html selectors in BS4), and assigning all the "news boxes" from THN to var news.
    content = session.get(url, verify=True).content 
    soup = beautsoup(content, 'html.parser')
    news = soup.find_all('div', {'class':'body-post'})

    # Main Execution for collecting each selector information, converting it into str format, and saving it into Django's SQLite3 DB.
    try:   # for THN only
        for news_item in news:
            main = news_item.find_all('a')[0]
            link = main['href']
            img_src = str(main.find('img')['data-src'])
            title_main = news_item.find('h2')
            title = str(title_main.text)
            find_date = news_item.find('div', {'class':'item-label'})
            item_date = str(find_date.text[1:-18]).strip('') # Strip the author's name and unnessary Unicode chars - just provide date

            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = img_src
            new_headline.date = item_date
            print(new_headline)

            try:
                new_headline.save()
            except Exception as e:
                print(e)

    except IntegrityError:
        print('Duplicate objects found. Ommitting and moving forward.')
    finally:   
        return redirect('../')

# Required for displaying each "news item" as a list in our home.html template file found in ../../templates/news/home.html
def list_news(request):
    primary_headlines = Headline.objects.all()[:6:1]
    reddit_headlines = Headline.objects.all()[7:13:1]
    context = {
        'object_list' : primary_headlines,
        'reddit_list' : reddit_headlines
        
    }
    
    return render(request, 'news/home.html', context) # Returns HTTP response whose contents are sent to news/home.html.
# context argument allows us to call the the list of news articles via home.html
