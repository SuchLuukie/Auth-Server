import flask
import os
from flask import request
from flask_restful import Api, Resource

from register import Register
from auth import Auth
from totp import Totp

os.system('cls')
app = flask.Flask(__name__)
api = Api(app)

api.add_resource(Register, "/register")
api.add_resource(Auth, "/auth")
api.add_resource(Totp, "/totp")
app.run(debug=True)