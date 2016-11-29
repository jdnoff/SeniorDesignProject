import json
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from Query_Parser import parseQuery
from Query_Parser import test_query
import academic_constants
from Author import *
from similarity_measure import jaccard_test
import Query_Parser
from TestResults.test_factory import get_evaluate_test_results


# Handler for the topic search use case

def do_topic_search(abstract):
	attributes = {
		academic_constants.ATT_AUTHOR_NAME,
		academic_constants.ATT_AUTHOR_ID,
		academic_constants.ATT_WORDS,
		academic_constants.ATT_PAPER_TITLE,
		academic_constants.ATT_CITATIONS
	}
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, 'latest', '15', '', attributes)
	real_data = evaluate_request(params)
	# real_data = get_evaluate_test_results()

	populated_authors = compile_author_list(real_data, keyword_list)
	search_list_of_authors(populated_authors, keyword_list)
	for author in populated_authors:
		author.scoreAuthor()
		author.sumCitations()
	return populated_authors


def search_list_of_authors(author_list, query_keywords):
	"""
	Performs an evaluate request on each author in a given list.
	:param authorname_list: a list of author names to be searched
	:return: a list of Author objects
	"""
	for author in author_list:
		query = "Composite({}={})".format(academic_constants.ATT_AUTHOR_ID, author.author_id)
		params = construct_params(query, 'latest', 25, '', {
			academic_constants.ATT_CITATIONS,
			academic_constants.ATT_WORDS,
			academic_constants.ATT_PAPER_TITLE,
			academic_constants.ATT_FIELD_OF_STUDY,
			academic_constants.ATT_YEAR,
			academic_constants.ATT_ID
		})
		data = evaluate_request(params)
		print(json.dumps(data))
		# Authors papers
		if 'entities' in data:
			for paper in data['entities']:
				p = AcademicPaper(paper[ATT_PAPER_TITLE].title())
				if ATT_WORDS in paper:
					p.addScore(jaccard_test(query_keywords['documents'][0]['keyPhrases'], paper[ATT_WORDS]))
					p.addKeywords(paper[ATT_WORDS])

				if ATT_CITATIONS in paper:
					p.addCitations(paper[ATT_CITATIONS])

				if ATT_YEAR in paper:
					p.year = paper[ATT_YEAR]
				# print(paper.title)
				author.addPaper(p)


def compile_author_list(data, query_keywords):
	"""
	Translates a json response into Author objects
	:param data: json response from Evaluate request
	:return: a list of Authors
	"""
	authors = {}
	if 'entities' in data:
		for paper in data['entities']:
			p = AcademicPaper(paper[ATT_PAPER_TITLE].title())
			if ATT_WORDS in paper:
				p.addScore(jaccard_test(query_keywords['documents'][0]['keyPhrases'], paper[ATT_WORDS]))
				p.addKeywords(paper[ATT_WORDS])
			p.addCitations(paper[ATT_CITATIONS])
			# print(paper[ATT_PAPER_TITLE],paper[ATT_CITATIONS])
			# Iterate through paper authors and create Authors
			for auth in paper['AA']:
				auth_id = auth['AuId']
				auth_name = auth['AuN']
				if auth_id in authors.keys():
					# If already present, add paper to Author
					authors[auth_id].addPaper(p)
				else:
					# Create new Author
					a = Author(author_name=auth_name, author_id=auth_id)
					a.addPaper(p)
					authors[auth_id] = a
	else:
		# bad response
		print("Bad response")

	ret = []
	i = 0
	for a in authors.keys():
		ret.append(authors[a])
		print("%d: %s" % (i, authors[a].author_name))
		i += 1
	return ret


def create_query(keyword_list):
	wordslist = []
	for key in keyword_list['documents'][0]['keyPhrases']:
		wrd = []
		for w in key.split(' '):
			wrd.append('W==\'{}\''.format(w))
		line = ','.join(wrd)
		wordslist.append('And({})'.format(line))
	# Or together and return
	keyword_query = 'Or({})'.format(','.join(wordslist))
	return 'And({},{})'.format(keyword_query, "Composite(F.FId=41008148)")


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
