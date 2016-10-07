import requests
from BaseClientMod import BaseClient
import sys

class getFriendsBdate(BaseClient):
	
	def response_handler(self, ID):
		bDateList = []

		response = requests.get('https://api.vk.com/method/friends.get?user_id={0}&fields=bdate&v=V'.format(ID)).json()
		if(response.get("response") == None):
			print("НЕТ")
			sys.exit()
		else:
			for x in response.get("response"):
				if(x.get("bdate") != None):
					if(len(x.get("bdate").split(".")) == 3):
						bDateList.append(2016 - int(x.get("bdate").split(".")[2], 10))
			return bDateList
