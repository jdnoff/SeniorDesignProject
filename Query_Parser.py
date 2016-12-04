# File which handles parsing a user query for key terms that
# can be sent to the Evaluate method

import json
import requests

# Use Key 1 for testing, Key 2 for Demos/etc.
API_KEY1 = '2188eefffbb2449f88b73e563deab172'
API_KEY2 = '62841b36e69d4c3eb4cddfdb7ac56b74'

# Jake's API keys
JAKE_API_KEY1 = 'd1ec02129efc4f1881d2d1bab395bf93'
JAKE_API_KEY2 = 'd711ea24618a4d91a5a4f05e7c89ea80'


# Analytic API Constants
KEYPHRASE_URL = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"
ANALYTICS_HEADERS = {'Content-Type': 'application/json',
                     'Ocp-Apim-Subscription-Key': JAKE_API_KEY1}

#Test Input demonstrating the format of an Analytics request
TEST_INPUT = {"documents": [
				{
					"language": "en",
					"id": "1",
					"text": "The increasing volume of data in modern business and science calls for more complex "
							"and sophisticated tools. Although advances in data mining technology have made "
							"extensive data collection much easier, it's still always evolving and there is a "
							"constant need for new techniques and tools that can help us transform this data into "
							"useful information and knowledge. Since the previous edition's publication, great "
							"advances have been made in the field of data mining. Not only does the third of "
							"edition of Data Mining: Concepts and Techniques continue the tradition of equipping "
							"you with an understanding and application of the theory and practice of discovering "
							"patterns hidden in large data sets, it also focuses on new, important topics in the "
							"field: data warehouses and data cube technology, mining stream, mining social "
							"networks, and mining spatial, multimedia and other complex data. Each chapter is a "
							"stand-alone guide to a critical topic, presenting proven algorithms and sound "
							"implementations ready to be used directly or with strategic modification against live "
							"data. This is the resource you need if you want to apply today's most powerful data "
							"mining techniques to meet real business challenges. * Presents dozens of algorithms "
							"and implementation examples, all in pseudo-code and suitable for use in real-world, "
							"large-scale data mining projects. * Addresses advanced topics such as mining "
							"object-relational databases, spatial databases, multimedia databases, time-series "
							"databases, text databases, the World Wide Web, and applications in several fields. "
							"*Provides a comprehensive, practical look at the concepts and techniques you need to "
							"get the most out of real business data"
				}
			] }

def construct_query(user_input):
	""" Function to insert user input into correct query format
		:return: json formatted query """
	query = { "documents": [
				{ "language": "en",
				  "id": "1",
				  "text": user_input
				}
			] }
	return query

def parseQuery(user_input):
	""" Function to generate a keyword list given user input
		:return: keyword list """
	response = requests.post(KEYPHRASE_URL, json=construct_query(user_input) , headers=ANALYTICS_HEADERS)
	data = response.json()
	word_list = data['documents'][0]['keyPhrases']
	word_list = word_list[0:16]
	return word_list

def test_query():
	""" Test function to get a stored result of a test query. Use to save requests.
		:return: keyword list """
	with open('Analytics_results_test') as data_file:
		return json.load(data_file)





