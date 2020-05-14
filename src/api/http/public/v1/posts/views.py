import logging
from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource

from hacker_news import dataclasses as dc, services as hn
from settings import API_POST_LIMIT

logger = logging.getLogger('hacker_news')


class HackerPostsResource(Resource):

    def get(self):
        """
        Get new posts with offset and limit and apply ordering

        - Limit and Offset params should be positive integers
        if limit > STORAGE_LIMIT or offset >= STORAGE_LIMIT,
        than new posts will be loaded and merged with previously saved posts and returned to
        client with limit and offset applied

        - Ordering applied to existing post attributes (id, title, url).
        if ordering params starts with "-" then descending order is used, otherwise - ascending
        -
        """
        limit_offset = {
            "limit": int(request.args.get('limit') or API_POST_LIMIT),
            "offset": int(request.args.get('offset') or 0)
        }

        if any([limit_offset['limit'] < 0, limit_offset['offset'] < 0]):
            return 'Limit and Offset should be postitive int', HTTPStatus.BAD_REQUEST

        order = request.args.get('order')

        posts = [
            {'id': p.id, 'title': p.title, 'url': p.url, 'saved_at': p.saved_at}
            for p in hn.get_posts(**limit_offset)
        ]

        logger.debug(f'Got {len(posts)} posts')

        if order and order.lstrip('-') in dc.HackerPost._fields:
            posts.sort(key=lambda p: p.get(order.lstrip('-')), reverse=order.startswith('-'))

        return jsonify(posts).json, HTTPStatus.OK
