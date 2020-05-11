import os

STORAGE_LIMIT = 30          # how many posts are stored
STORAGE_REFRESH_RATE = int(os.environ.get('STORAGE_REFRESH_RATE', 60))
API_POST_LIMIT = 5
API_PREFIX = ''             # API prefix
