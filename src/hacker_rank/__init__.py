import logging

logger = logging.getLogger('hacker_rank')
fmt = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel('DEBUG')
