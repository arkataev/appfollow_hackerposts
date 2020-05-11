import hacker_rank.services
from hacker_rank import services as hr
from settings import STORAGE_LIMIT


def refresh_posts_storage():
    """Fetch new posts from external source an save to storage"""
    posts = hacker_rank.services.gateway.fetch_new_posts()
    hr.refresh_posts(posts[:STORAGE_LIMIT])
