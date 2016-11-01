import json
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from Query_Parser import parseQuery
from Query_Parser import test_query
import academic_constants
from Author import *


# Handler for the topic search use case

def do_topic_search(abstract):
	attributes = {academic_constants.ATT_AUTHOR_NAME, academic_constants.ATT_AUTHOR_ID}
	# TODO: Send abstract to query processor instead of test_query
	# keyword_list = test_query()
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, 'latest', '5', '', attributes)
	data = evaluate_request(params)
	# data = get_test_results('author_result_example')
	return search_list_of_authors(compile_author_list(data))


def search_list_of_authors(authorname_list):
	author_list = []
	for auth in authorname_list:
		query = "Composite({}={})".format(academic_constants.ATT_AUTHOR_ID, authorname_list[auth])
		params = construct_params(query, 'latest', 5, '', {
			academic_constants.ATT_CITATIONS,
			academic_constants.ATT_WORDS,
			academic_constants.ATT_PAPER_TITLE,
			academic_constants.ATT_FIELD_OF_STUDY,
		})
		data = evaluate_request(params)
		# data = get_test_results('author_result_example')
		print(json.dumps(data))
		a = Author(auth, authorname_list[auth], data)
		author_list.append(a)
	return author_list


def compile_author_list(data):
	ret = {}
	if 'entities' in data:
		for paper in data['entities']:
			for auth in paper['AA']:
				ret[auth['AuN']] = auth['AuId']
	else:
		# bad response
		print("Bad response")

	return ret


def create_query(keyword_list):
	wordslist = []
	for key in keyword_list['documents'][0]['keyPhrases']:
		wrd = []
		for w in key.split(' '):
			wrd.append('W==\'{}\''.format(w))
		line = ','.join(wrd)
		wordslist.append('And({})'.format(line))
	return wordslist[0]


def get_test_results(file):
	with open(file) as data_file:
		return json.load(data_file)


def test_methods():
	print(create_query(test_query()))
	for res in compile_author_list(get_test_results('AS_example_result')):
		print(res)


def testMakeAuthors():
	brybry = 2203702053
	data = get_test_results("author_result_example.txt")
	auth = Author("test Author", brybry, data)
	print(auth.author_name)
	print("words:")
	for w in auth.keyWords:
		print(w)

	print("Titles")
	for ti in auth.paperTitles:
		print(ti)

	print("fields of study")
	for fs in auth.fieldsOfStudy:
		print(fs)
	ret = [auth]
	return ret


# print(json.dumps(get_test_results("author_result_example.txt"),indent=4))
testMakeAuthors()
