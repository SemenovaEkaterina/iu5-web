import requests
from Base_Client_Mod import BaseClient
import sys

class GetUserId:

	BASE_URL = 'https://api.vk.com/method/'
	method = None

	def __init__(self, identifier):
		self.method = 'users.get?user_ids={0}&v=V'.format(identifier)

	
	def generate_url(self, method):
		return '{0}{1}'.format(self.BASE_URL, method)


	def _get_data(self, method):
		response = None
		
		response = requests.get(self.generate_url(method))      	

		return self.response_handler(response)
	

	def response_handler(self, response):

		if response.json().get("response") is None or len(response.json().get("response")) == 0:
			return []
		return response.json().get("response")[0].get("uid")


	def execute(self):
		return self._get_data(self.method)
