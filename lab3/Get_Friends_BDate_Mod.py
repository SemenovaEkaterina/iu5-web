import requests
from Base_Client_Mod import BaseClient
import datetime



class GetFriendsBdate(BaseClient):
	
	BASE_URL = 'https://api.vk.com/method/'
	method = None

	def __init__(self, ID):
		self.method = 'friends.get?user_id={0}&fields=bdate&v=V'.format(ID)

	
	def generate_url(self, method):
		return '{0}{1}'.format(self.BASE_URL, method)


	def _get_data(self, method):
		response = None
		
		response = requests.get(self.generate_url(method))      	

		return self.response_handler(response)
	

	def response_handler(self, response):
		bDateList = []

		now = datetime.datetime.now()

		if response.json().get("response") is None:
			return []
			
		else:
			for x in response.json().get("response"):
				if(x.get("bdate") != None):
					if(len(x.get("bdate").split(".")) == 3):
						bDateList.append(now.year - int(x.get("bdate").split(".")[2], 10))
			return bDateList


	def execute(self):
		return self._get_data(self.method)
