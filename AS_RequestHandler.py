import requests
import json
from academic_constants import *

""" url request should be in the form of
https://api.projectoxford.ai/academic/v1.0/evaluate[?expr][&model][&count][&offset][&orderby][&attributes]
"""

"""Interpret URL should be
https://api.projectoxford.ai/academic/v1.0/interpret[?query][&complete][&count][&offset][&timeout][&model]
"""


def interpret_request(user_input):
	"""
	Constructs an interpret query given a user search term
	:param user_input: User entered search term
	:return: JSON reponse of Microsoft Academic
	"""
	params = {'query': user_input, PARAM_COUNT: '10', PARAM_MODEL: 'latest'}
	response = requests.get(INTERPRET_URL, headers=REQUEST_HEADER, params=params)
	return response.json()


def evaluate_request(params):
	"""
	Sends an evaluate request to the Academic Knowledge API and returns the JSON string from the request.
	:param params: A list of parameters
	:return: The JSON response
	"""
	response = requests.get(EVALUATE_URL, headers=REQUEST_HEADER, params=params)
	return response.json()


def histogram_request(params):
	"""
	Sends a calchistogram request to the Academic Knowledge API and returns teh JSON string from the request
	:param params:
	:return:
	"""
	response = requests.get(HIST_URL, headers=REQUEST_HEADER, params=params)
	return response.json()


def construct_params(exp, model, count, order, atts):
	"""
	Constructs a request parameter string for Calchistogram and Evaluate. Interpret follows a different format.
	:param exp: A query expression that specifies which entities should be returned.
	:param model: Name of the model that you wish to query. Currently, the value defaults to "latest".
	:param count: Number of results to return.
	:param order: Name of an attribute that is used for sorting the entities. Optionally, ascending/descending can
	be specified. The format is: name:asc or name:desc.
	:param atts: A comma delimited list that specifies the attribute values that are included in the response. Attribute
	names are case-sensitive.
	:return: a list containing request parameters as pairs
	"""
	params = {PARAM_EXPR: exp, PARAM_MODEL: model, PARAM_COUNT: count,
	          PARAM_ORDERBY: order, PARAM_ATTRIBUTES: atts}
	return params

