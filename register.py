import json
import random
import pyotp
from flask_restful import Api, Resource
from flask import request

from encryptor import Encryptor

class Register(Resource):
	def __init__(self):
		self.encryptor = Encryptor()

	def post(self):
		data = request.get_json(force=True)

		if self.valid_request(data):
			if not self.email_in_database(data):
				self.register_to_database(data)
				return {"success": True}

		return {"success": False}


	def register_to_database(self, data):
		salt = self.encryptor.salter()
		iterations = random.randint(600000, 700000)
		encrypted_password = self.encryptor.hasher(data["password"], salt, iterations)

		data = {
			"email": data["email"],
			"password": encrypted_password,
			"salt": salt,
			"iterations": iterations,
			"TOTP": pyotp.random_base32()
		}

		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		database.append(data)
		with open("database.json", 'w') as f:
			json.dump(database, f, indent=4)


	def valid_request(self, data):
		valid = ["email", "password"]
		count = 0

		for line in data:
			if not line == valid[count]:
				return False
			count += 1
		return True


	def email_in_database(self, data):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["email"] == data["email"]:
				return True
		return False