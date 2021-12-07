from flask import Flask
from flask_restplus import Api

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
            version='1.0',
            title='API Airport',
            description='API AmoPromo Challenge',
            doc='/docs'
        )

    def run(self):
        self.app.run(debug=True)

server = Server()