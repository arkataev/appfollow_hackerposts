from flask import Flask
from flask_restful import Api

from api.http.public.v1.posts.urls import urls
from settings import API_PREFIX

app = Flask(__name__)
api = Api(app, prefix=API_PREFIX)


for url in urls:
    api.add_resource(*url)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
