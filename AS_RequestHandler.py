import concurrent

import requests
import json

# Constants
QUERY_PARAM = 'expr'
MODEL_PARAM = 'model'
COUNT_PARAM = 'count'
ORDERBY_PARAM = 'orderby'
ATTRIBUTES_PARAM = 'attributes'
header = {'Ocp-Apim-Subscription-Key': '5569c93188b746fcab48355fa04a68f8'}
EVALUATE_URL = 'https://api.projectoxford.ai/academic/v1.0/evaluate'
INTERPRET_URL = 'https://api.projectoxford.ai/academic/v1.0/interpret'

""" url request should be in the form of
https://api.projectoxford.ai/academic/v1.0/evaluate[?expr][&model][&count][&offset][&orderby][&attributes]
"""


"""Interpret URL should be
https://api.projectoxford.ai/academic/v1.0/interpret[?query][&complete][&count][&offset][&timeout][&model]
"""


def construct_query(user_input):
    """
    Constructs a query given a user search term
    :param user_input: User entered search term
    :return: JSON reponse of Microsoft Academic
    """
    params = {'query': user_input, COUNT_PARAM: '10', MODEL_PARAM: 'latest'}
    response = requests.get(INTERPRET_URL, headers=header, params=params)
    return response.json()


def construct_params(query, model, count, orderby, attributes):
    """
    :param query: A query expression that specifies which entities should be returned.
    :param model: Name of the model that you wish to query. Currently, the value defaults to "latest".
    :param count: Number of results to return.
    :param orderby: Name of an attribute that is used for sorting the entities. Optionally, ascending/descending can
    be specified. The format is: name:asc or name:desc.
    :param attributes: A comma delimited list that specifies the attribute values that are included in the response. Attribute
    names are case-sensitive.
    :return: a list containing request parameters as pairs
    """
    params = {QUERY_PARAM: query, MODEL_PARAM: model, COUNT_PARAM: count,
              ORDERBY_PARAM: orderby, ATTRIBUTES_PARAM: attributes}
    return params


def evaluate_request(params):
    """
    Sends a request to the Academic Knowledge API and returns the JSON string from the request.
    :param params: A list of parameters
    :return: The JSON response
    """
    response = requests.get(EVALUATE_URL, headers=header, params=params)
    return response.json()


attributes = {'Ti', 'AA.AuN', 'Id'}

# Test method
def main():
    p = construct_params("and(composite(AA.AuN='brian davison'),Y>2005)", 'latest', '10', '', attributes)
    res = evaluate_request(p)

    print(res.keys())
    query = construct_query("brian davison")
    print(query.keys())
    print("QUERY\n")

    # print(query['interpretations'].value)
    print(query['interpretations'][1]['rules'][0]['output']['value'])
    print(json.dumps(query, indent=4))
    print("REQUEST\n")
    # print(json.dumps(res, indent=4))


def query(user_text):
    q = construct_query(user_text)
    value = q['interpretations'][1]['rules'][0]['output']['value']

    # Use value to send evaluate request
    p = construct_params(value, 'latest', '10', '', attributes)
    res = evaluate_request(p)

    return res['entities']


def test_query():
    """
    Test method to generate a results list
    :return: result list
    """
    with open('results_example.txt') as data_file:
        return json.load(data_file)


print(json.dumps(query("brian davison")))
