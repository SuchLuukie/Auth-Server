import string
import random
import hashlib

class Encryptor():
	def __init__(self):
		self.chars = list(string.printable)
		del self.chars[-6:]

		self.salt_length = 32

	def hasher(self, password, salt, iterations):
		salted_passwd = salt + password
		for i in range(iterations):
			salted_passwd = salted_passwd.encode("utf8")
			salted_passwd = hashlib.sha512(salted_passwd).hexdigest()

		return salted_passwd


	def salter(self):
		salt = ""
		for i in range(self.salt_length):
			salt += random.choice(self.chars)
		return salt