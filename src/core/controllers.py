from hacker_news import services as hn
from settings import STORAGE_LIMIT


def refresh_posts_storage():
    """Fetch new posts from external source an save to storage"""
    posts = hn.gateway.fetch_new_posts()
    hn.refresh_posts(posts[:STORAGE_LIMIT])
