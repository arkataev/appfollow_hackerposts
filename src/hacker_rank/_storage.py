import os

import pymongo

mongo = pymongo.MongoClient(host='host.docker.internal', port=27017)
mongo.admin.authenticate(os.environ.get('DB_USER'), os.environ.get('DB_PASS'))
