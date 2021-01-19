import pyotp
import json
from flask_restful import Api, Resource
from flask import request

class Totp(Resource):
	def post(self):
		data = request.get_json(force=True)

		if self.valid_post(data):
			if self.in_database(data):
				return {"success": self.TOTP_check(data)}

		return {"success": False}


	def TOTP_check(self, data):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["password"] == data["password"]:
				secret = user["TOTP"]
				totp = pyotp.TOTP(secret)
				return totp.verify(data["code"])


	def in_database(self, data):
		with open("database.json", "r") as json_file:
			database = json.load(json_file)

		for user in database:
			if user["password"] == data["password"]:
				return True

		return False


	def valid_post(self, data):
		valid = ["password", "code"]
		count = 0

		for line in data:
			if not line == valid[count]:
				return False
			count += 1
		return True