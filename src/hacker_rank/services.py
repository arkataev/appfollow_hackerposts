import logging
from operator import itemgetter
from typing import List

from common.http.clients import SimpleHttpClient
from hacker_rank._controllers import HackerRankGateway
from settings import STORAGE_LIMIT
from . import _storage, _utils, dataclasses as dc

logger = logging.getLogger('hacker_rank')

gateway = HackerRankGateway(SimpleHttpClient())


def refresh_posts(posts: List[dc.HackerPost]):
    """Clean storage and save new posts"""
    _storage.mongo.appfollow.hacker_posts.drop()
    _storage.mongo.appfollow.hacker_posts.insert_many(
        [{'id': p.id, 'title': p.title, 'url': p.url, 'time': p.time} for p in posts]
    )


def get_posts(limit=0, offset=0) -> List[dc.HackerPost]:
    """
    Fetch posts from storage.

    If limit or offset is greater than STORAGE_LIMIT
    than new posts will be loaded from external resource
    and appened to posts fetched from the storage
    """

    posts = _storage.mongo.appfollow.hacker_posts.find(
        sort=[('time', _storage.pymongo.ASCENDING)],
    )
    attrs = itemgetter(*dc.HackerPost._fields[:-1])
    posts = [dc.HackerPost(*attrs(p), p['_id'].generation_time) for p in posts]

    if offset + limit >= STORAGE_LIMIT:
        _new_posts = gateway.fetch_new_posts()
        posts = _utils.merge_longest_posts(posts, _new_posts, limit=limit + offset)

    return posts[offset:offset + limit]
