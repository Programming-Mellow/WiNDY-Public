import feedparser
from datetime import datetime, timedelta
import pytz  # Add this import

# Define Central Time timezone
CENTRAL_TZ = pytz.timezone('America/Chicago')

# RSS Feed URLs as constants (for testing)
zdnet = "https://www.zdnet.com/news/rss.xml"
the_new_stack = "https://thenewstack.io/feed"
ars_technica = "https://feeds.arstechnica.com/arstechnica/index"
bbc = "http://feeds.bbci.co.uk/news/rss.xml?edition=int"

def parse_and_add(website, lst):
    # Calculate cutoff time: 6 AM yesterday in Central Time
    now = datetime.now(CENTRAL_TZ)
    yesterday_6am = now.replace(hour=6, minute=0, second=0, microsecond=0) - timedelta(days=1)
    
    web_feed = feedparser.parse(website)
    
    for entry in web_feed.entries:
        # Check if entry has a published date
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            # Convert published time to datetime in UTC, then to Central Time
            published_time = datetime(*entry.published_parsed[:6], tzinfo=pytz.UTC)
            published_time_ct = published_time.astimezone(CENTRAL_TZ)
            
            # Only add articles published after 6 AM yesterday Central Time
            if published_time_ct >= yesterday_6am:
                article_data = f"{entry.title} (<{entry.link}>)"
                lst.append(article_data)
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            # Fallback to updated time if published not available
            updated_time = datetime(*entry.updated_parsed[:6], tzinfo=pytz.UTC)
            updated_time_ct = updated_time.astimezone(CENTRAL_TZ)
            
            if updated_time_ct >= yesterday_6am:
                article_data = f"{entry.title} (<{entry.link}>)"
                lst.append(article_data)
        else:
            # If no date available, include it (fallback behavior)
            article_data = f"{entry.title} (<{entry.link}>)"
            lst.append(article_data)
    
    return lst