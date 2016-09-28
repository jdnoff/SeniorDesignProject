import concurrent

import requests
import json

# Constants
QUERY_PARAM = 'expr'
MODEL_PARAM = 'model'
COUNT_PARAM = 'count'
ORDERBY_PARAM = 'orderby'
ATTRIBUTES_PARAM = 'attributes'
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
    header = {'Ocp-Apim-Subscription-Key': '5569c93188b746fcab48355fa04a68f8'}
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
    header = {'Ocp-Apim-Subscription-Key': '5569c93188b746fcab48355fa04a68f8'}
    response = requests.get(EVALUATE_URL, headers=header, params=params)
    return response.json()


# Test method
def main():
    p = construct_params("and(composite(AA.AuN='brian davison'),Y>2005)", 'latest', '10', '', {'Ti', 'AA.AuN', 'Id'})
    res = evaluate_request(p)
    query = construct_query("brian davison")
    print("QUERY\n")
    print(json.dumps(query, indent=4))
    print("REQUEST\n")
    print(json.dumps(res, indent=4))


main()
