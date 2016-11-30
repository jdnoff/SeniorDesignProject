import json
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from Query_Parser import parseQuery
from Query_Parser import test_query
import academic_constants
from Author import *
from similarity_measure import jaccard_test
from similarity_measure import keySplit
import Query_Parser
from TestResults.test_factory import get_evaluate_test_results
from nltk.corpus import stopwords

"""
IMPORTANT: run this function and download stopwords corpus from the window:
				nltk.download()
"""

# Handler for the topic search use case
def do_topic_search(abstract):
	"""
	Handler for the topic search use case
	:param abstract: full text of a paper abstract
	:return: List of Authors ready to be displayed
	"""
	attributes = {
		academic_constants.ATT_AUTHOR_NAME,
		academic_constants.ATT_AUTHOR_ID,
		academic_constants.ATT_WORDS,
		academic_constants.ATT_PAPER_TITLE,
		academic_constants.ATT_CITATIONS
	}
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, '', '10', '', attributes)
	real_data = evaluate_request(params)
	# real_data = get_evaluate_test_results()

	populated_authors = compile_author_list(real_data)
	search_list_of_authors(populated_authors, keyword_list)

	# Compute scores for each author before sending them to be displayed
	for author in populated_authors:
		author.scoreAuthor()
		author.sumCitations()
		author.computeMostRecentYear()
		author.totalScore()
	populated_authors.sort(key=lambda author: author.cumulativeScore,reverse=True)
	return populated_authors


# 2
def search_list_of_authors(author_list, query_keywords):
	"""
	Performs an evaluate request on each author in a given list.
	:param author_list: a list of author names to be searched
	:return: a list of Author objects
	"""
	cachedStopWords = stopwords.words("english")
	for author in author_list:
		query = "Composite({}={})".format(academic_constants.ATT_AUTHOR_ID, author.author_id)
		params = construct_params(query, 'latest', 8, '', {
			academic_constants.ATT_CITATIONS,
			academic_constants.ATT_WORDS,
			academic_constants.ATT_PAPER_TITLE,
			academic_constants.ATT_FIELD_OF_STUDY,
			academic_constants.ATT_YEAR,
			academic_constants.ATT_EXTENDED,
			academic_constants.ATT_ID,
			"RId",
			"E"
		})
		data = evaluate_request(params)
		# print(json.dumps(data, indent=1))
		# Authors papers
		if 'entities' in data:
			for paper in data['entities']:
				p = AcademicPaper(paper[ATT_PAPER_TITLE].title())
				#if ATT_WORDS in paper:
					#p.addScore(jaccard_test(query_keywords, paper[ATT_WORDS]))
					#p.addKeywords(paper[ATT_WORDS])

				if ATT_CITATIONS in paper:
					p.addCitations(paper[ATT_CITATIONS])

				if ATT_EXTENDED in paper:
					desc = json.dumps(paper[ATT_EXTENDED])
					try:
						desc = desc.split('\\"')
						if desc[5] == 'D':
							p.addDesc(desc[7])
							abKey = keySplit(parseQuery(desc[7]),cachedStopWords)
							queryKeys = keySplit(query_keywords, cachedStopWords)
							p.addKeywords(abKey)
							score = jaccard_test(queryKeys,abKey)
							p.addScore(score)

						else:
							p.addDesc("none")
					except:
						print("No Abstract")
						break

				if ATT_YEAR in paper:
					p.year = paper[ATT_YEAR]
				# print(paper.title)
				author.addPaper(p)


# 1
def compile_author_list(data):
	"""
	This is the first step of our query. Translates a json response of papers into a list of Authors
	:param data: json response from Evaluate request
	:param query_keywords: keywords parsed from the query
	:return: a list of Authors
	"""
	authors = {}
	if 'entities' in data:
		for paper in data['entities']:
			# Iterate through paper authors and create Authors
			for auth in paper['AA']:
				auth_id = auth['AuId']
				auth_name = auth['AuN']
				if auth_id not in authors.keys():
					# Create new Author
					a = Author(author_name=auth_name, author_id=auth_id)
					authors[auth_id] = a
	else:
		# bad response
		print("Bad response")

	ret = []
	i = 0
	for a in authors.keys():
		ret.append(authors[a])
		# print("%d: %s" % (i, authors[a].author_name))
		i += 1
	return ret


def create_query(keyword_list):
	"""
	Creates the query used by topic search to find the initial list of authors
	:param keyword_list: A list of keywords that were parsed from the abstract
	:return: A query string formatted for use with microsoft academic
	"""
	cachedStopWords = stopwords.words("english")
	wordslist = []
	for key in keyword_list:
		wrd = []
		for w in key.split(' '):
			if w not in cachedStopWords:
				wrd.append('W==\'{}\''.format(w))
		line = ','.join(wrd)
		wordslist.append('And({})'.format(line))
	# Or together and return
	keyword_query = 'Or({})'.format(','.join(wordslist))
	return 'And({},{})'.format(keyword_query, "Composite(F.FId=41008148)")
