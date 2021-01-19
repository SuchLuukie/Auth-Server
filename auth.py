import json
from flask_restful import Api, Resource
from flask import request

from encryptor import Encryptor

class Auth(Resource):
	def __init__(self):
		self.encryptor = Encryptor()

	def post(self):
		data = request.get_json(force=True)

		if self.valid_request(data):
			if self.email_in_database(data):
				info = self.get_info(data)
				encrypted_password = self.encryptor.hasher(data["password"], info["salt"], info["iterations"])

				if self.password_in_database(encrypted_password):
					return {"success": True, "info": encrypted_password}

		return {"success": False}


	def password_in_database(self, password):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["password"] == password:
				return True

		return False


	def get_info(self, data):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["email"] == data["email"]:
				return user


	def email_in_database(self, data):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["email"] == data["email"]:
				return True

		return False


	def valid_request(self, data):
		valid = ["email", "password"]
		count = 0

		for line in data:
			if not line == valid[count]:
				return False
			count += 1
		return True