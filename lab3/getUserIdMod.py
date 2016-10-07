import requests
from BaseClientMod import BaseClient
import sys

class getUserId:
	
	def response_handler(self, identifier):
		response = requests.get('https://api.vk.com/method/users.get?user_ids={0}&v=V'.format(identifier)).json()
		if response.get("response") == None or len(response.get("response")) == 0:
			print("НЕТ")
			sys.exit()
		return response.get("response")[0].get("uid")
