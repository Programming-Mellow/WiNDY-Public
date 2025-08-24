# Main file which consolidates all commands from the subfolders altogether to help run the Discord bot (WiNDY) as needed.

from dotenv import load_dotenv
from datetime import datetime
import pytz
from data.rss_handler import parse_and_add as paa
from data.api_handler import tasks1 as ct
from data.api_handler import tasks2 as wpt
from data.api_handler import tasks3 as pt
from ml.predict import prediction

# Load environment variables
load_dotenv()

# Define Central Time timezone
CENTRAL_TZ = pytz.timezone('America/Chicago')

# RSS Feeds as a dictionary
rss_feeds = {
    "zdnet": "https://www.zdnet.com/news/rss.xml",
    "the_new_stack": "https://thenewstack.io/feed",
    "ars_technica": "https://feeds.arstechnica.com/arstechnica/index",
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml?edition=int"
}

# Dictionary to store best article from each source
best_articles = {}

def check_work_sched():
    # Get current day name in Central Time
    today = datetime.now(CENTRAL_TZ).strftime("%A")

    if today == "Monday":
        workplace = 'NOTION_DASHBOARD1'
    elif today not in ["Tuesday", "Wednesday", "Thursday"]:
        workplace = 'NOTION_DASHBOARD2'
    else:
        workplace = 'NOTION_DASHBOARD3'
    
    return workplace

def on_run():
    # Clear previous articles
    best_articles.clear()
    
    # Group articles by source
    articles_by_source = {}
    
    # Fetch latest article titles from various websites
    for name, url in rss_feeds.items():
        source_articles = []
        paa(url, source_articles)
        articles_by_source[name] = source_articles
    
    # Run prediction for each source and get the best article
    for source_name, articles in articles_by_source.items():
        if articles:
            best_article = prediction(articles)
            best_articles[source_name] = best_article

    # Check what day it is and correspond it to correct dashboard
    tasks1 = []
    tasks2 = []
    tasks3 = []
    workplace = check_work_sched()
    ct('NOTION_DASHBOARD1', tasks1)
    wpt(workplace, tasks2)
    pt('NOTION_DASHBOARD4', tasks3)

    article_list = []
    for article in best_articles.values():
        article_list.append(article)

    return {
        'articles': article_list,
        'tasks_1': tasks1,
        'tasks_2': tasks2,
        'tasks_3': tasks3
    }

def format_daily_message():
    data = on_run()
    
    message = "# **Good morning! 😎**\n\n\n"
    message += "## **📋 Ready to get started today? Here are your tasks for today:**\n"
    
    message += "> **__Tasks 1__**\n"
    for task in data['tasks_1']:
        message += f"> {task}\n"
    message += "> \n"

    message += "> **__Tasks 2__**\n"
    for task in data['tasks_2']:
        message += f"> {task}\n"
    message += "> \n"

    message += "> **__Tasks 3__**\n"
    for task in data['tasks_3']:
        message += f"> {task}\n"
    message += "> \n"

    message += "## **📰 Itching for knowledge and keeping up with the world? I've prepped some articles for you:**\n"
    for article in data['articles']:
        message += f"> *{article}*\n"
    
    message += "## **Enjoy your day! ✨**"
    
    return message