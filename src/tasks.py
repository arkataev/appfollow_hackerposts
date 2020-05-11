import logging
from datetime import timedelta

from timeloop import Timeloop

from core.controllers import refresh_posts_storage
from settings import STORAGE_REFRESH_RATE

logger = logging.getLogger('hacker_rank')

tl = Timeloop()


@tl.job(interval=timedelta(minutes=STORAGE_REFRESH_RATE))
def update_posts_storage_tasks():

    try:
        refresh_posts_storage()
    except Exception as e:
        logger.exception(e)
    else:
        logger.info('Posts storage updated')


if __name__ == '__main__':
    tl.start(block=True)
