import json
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from Query_Parser import parseQuery
import academic_constants
from Author import *

# Handler for the topic search use case

def do_topic_search(abstract):
	attributes = {academic_constants.ATT_AUTHOR_NAME}
	# TODO: Send abstract to query processor instead of test_query
	# keyword_list = test_query()
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, 'latest', '11', '', attributes)
	data = evaluate_request(params)
	return search_list_of_authors(compile_author_list(data))


def search_list_of_authors(authorname_list):
	author_list = []
	for auth in authorname_list:
		query = "Composite({}==\'{}\')".format(academic_constants.ATT_AUTHOR_NAME, auth)
		params = construct_params(query, 'latest', 10, '', {
			academic_constants.ATT_CITATIONS,
			academic_constants.ATT_WORDS,
			academic_constants.ATT_PAPER_TITLE,
			academic_constants.ATT_FIELD_OF_STUDY
		})
		data = evaluate_request(params)
		print(json.dumps(data))
		a = Author(auth, data)
		author_list.append(a)
	return author_list



def compile_author_list(data):
	ret = []
	for paper in data['entities']:
		for auth in paper['AA']:
			ret.append(auth['AuN'])
	return ret


# STUB
def create_query(keyword_list):
	wordslist = []
	for key in keyword_list['documents'][0]['keyPhrases']:
		wrd = []
		for w in key.split(' '):
			wrd.append('W==\'{}\''.format(w))
		line = ','.join(wrd)
		wordslist.append('And({})'.format(line))
	return wordslist[0]


def get_test_results():
	with open('AS_example_result') as data_file:
		return json.load(data_file)


def test_methods():
	print(create_query(test_query()))
	for res in compile_author_list(get_test_results()):
		print(res)
