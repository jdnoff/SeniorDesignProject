# File which handles parsing a user query for key terms that
# can be sent to the Evaluate method

import json
import requests

# Joe's API keys
API_KEY1 = '2188eefffbb2449f88b73e563deab172'  # <---- This one is dead
API_KEY2 = '62841b36e69d4c3eb4cddfdb7ac56b74'  # <---- also dead

# Jake's API keys
JAKE_API_KEY1 = 'd1ec02129efc4f1881d2d1bab395bf93' # <---- currently in use
JAKE_API_KEY2 = 'd711ea24618a4d91a5a4f05e7c89ea80'

# Analytic API Constants
KEYPHRASE_URL = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"
ANALYTICS_HEADERS = {'Content-Type': 'application/json',
                     'Ocp-Apim-Subscription-Key': JAKE_API_KEY1}

def construct_query(user_input):
	""" Function to insert user input into correct query format
		:return: json formatted query
	"""
	query = { "documents": [
				{ "language": "en",
				  "id": "1",
				  "text": user_input
				}
			] }
	return query

def parseQuery(user_input):
	""" Function to generate a keyword list given user input
		:return: keyword list
	"""
	response = requests.post(KEYPHRASE_URL, json=construct_query(user_input) , headers=ANALYTICS_HEADERS)
	data = response.json()
	word_list = []
	if 'documents' in data:
		word_list = data['documents'][0]['keyPhrases']
		# takes the first 16 keywords returned, eliminates some less relevant keywords in most abstracts.
		# if a keyword list has less than 16 words, all of the words are used.
		word_list = word_list[0:16]
	return word_list





