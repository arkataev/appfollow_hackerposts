import logging
import threading
import time
from typing import List

from common.http import clients
from hacker_rank import dataclasses as dc

logger = logging.getLogger('hacker_rank')


class GatewayError(Exception):
    pass


class NoData(GatewayError):
    pass


class HackerRankGateway:
    """
    Hacker news API gateway.

    Provides API for fetching new posts from hacker-news
    """
    base_url = 'https://hacker-news.firebaseio.com/v0'
    posts_cache_limit = 500
    workers = 50

    def __init__(self, client: clients.SimpleHttpClient):
        self._client = client
        self._posts_cache = {}

    def clean_cache(self, full_clean=False):
        """

        """
        if not full_clean:
            for _ in range(self.posts_cache_limit // 2):
                self._posts_cache.popitem()
        else:
            self._posts_cache = {}

    def fetch_post(self, post_uid: int) -> dc.HackerPost:
        """
        Get post data for provided post uid

        :raise GatewayError: if post_uid not found
        """

        post = self._posts_cache.get(post_uid)

        if not post:

            data = self.fetch_url(f'{self.base_url}/item/{post_uid}.json')
            post = dc.HackerPost(
                id=data.get('id'),
                title=data.get('title'),
                url=data.get('url'),
                time=data.get('time')
            )

            if len(self._posts_cache) >= self.posts_cache_limit:
                self.clean_cache()

            self._posts_cache[post.id] = post

        return post

    def fetch_new_posts(self) -> List[dc.HackerPost]:
        """Get up to 500 new posts ids. List length is not guaranteed"""
        post_uids = self.fetch_url(f'{self.base_url}/newstories.json')
        posts = self.fetch_posts_uids(post_uids)

        return posts

    def fetch_url(self, url: str):
        """

        :raise GateWayError: if no data was fetched
        """
        try:
            response = self._client.send(method='GET', url=url)
        except clients.HttpClientError as e:
            raise GatewayError(f'Could not fetch url.\n{e}')

        data = response.json()

        if not data:
            raise NoData(f'No data for {url}')

        return data

    def fetch_posts_uids(self, post_uids: List[int]) -> List[dc.HackerPost]:
        """

        :param post_uids:
        :raise GatewayError: if no data was fetched
        :return: sorted by creation time list of posts
        """
        result = []
        threads = []

        def _fetch_posts(posts: list, results: list):
            while True:

                try:
                    post_uid = posts.pop()
                except IndexError:
                    break

                try:
                    post = self.fetch_post(post_uid)
                except GatewayError as e:
                    logger.warning(e)
                else:
                    results.append(post)

        start = time.time()

        for _ in range(self.workers):
            t = threading.Thread(target=_fetch_posts, args=(post_uids, result))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        end = time.time()

        logger.debug(f'{len(result)} posts fetched in {end-start}')

        if not result:
            raise NoData('No posts to fetch')

        # number of posts is limited to 500 by external resource,
        # so sorting is rather cheap operation here otherwise we should optimize.
        return sorted(result, key=lambda p: p.time)
