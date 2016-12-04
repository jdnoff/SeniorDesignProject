import json
from AS_RequestHandler import construct_params, evaluate_request
from Query_Parser import parseQuery
import academic_constants
from Author import *
from similarity_measure import jaccard_test, keySplit, cosine_sim
from TestResults.test_factory import get_evaluate_test_results
from nltk.corpus import stopwords
from django.core.cache import cache
from Corpus import *

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

	#NEW: create corpus from query words
	docs = {}
	cachedStopWords = stopwords.words("english")
	query = TextBlob(abstract.lower())
	docs[-1] = query
	corpWords = []
	for word in query.words:
		if word not in cachedStopWords and word not in corpWords:
				corpWords.append(word)

	#Initial AS Query
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, '', '4', '', attributes)
	real_data = evaluate_request(params)
	# real_data = get_evaluate_test_results()

	#Get Author information
	authorId_list = compile_author_list(real_data)
	populated_authors = search_list_of_authors(authorId_list, keyword_list)

	#NEW: construct tf-idf vectors from documents
	for author in populated_authors:
		for paper in author.papers:
			if paper.id not in docs.keys():
				docs[paper.id] = TextBlob(paper.desc.lower())
	corpus = Corpus(docs, corpWords)
	corpus.constructVectors()

	#NEW: cosine similarity
	query = corpus.scoredDocs[0].vector

	# original doc has id of -1
	for doc in corpus.scoredDocs:
		if doc.id == -1:
			query = doc.vector
	docDict = {}
	for document in corpus.scoredDocs:
		sim = cosine_sim(query, document.vector)
		document.addScore(sim)
		docDict[document.id] = sim
		print(document.id, ": ", document.score)

	# Compute scores for each author before sending them to be displayed
	for author in populated_authors:
		author.scoreAuthor()
		author.sumCitations()
		author.computeMostRecentYear()
		author.totalScore()
		author.setTfidfScore(docDict)

	populated_authors.sort(key=lambda author: author.cumulativeScore, reverse=True)
	return populated_authors


# 2
def search_list_of_authors(author_list, query_keywords):
	"""
	Performs an evaluate request on each author in a given list.
	:param author_list: a list of author names to be searched
	:return: a list of Author objects
	"""
	cachedStopWords = stopwords.words("english")
	queryKeys = keySplit(query_keywords, cachedStopWords)
	authors = []
	for aId in author_list.keys():
		# Check cache
		cachedAuthor = cache.get(aId)
		if not cachedAuthor:
			# Cache miss
			print(author_list[aId], " Not in cache, searching microsoft")
			author = Author(author_list[aId], aId)
			query = "Composite({}={})".format(academic_constants.ATT_AUTHOR_ID, aId)
			params = construct_params(query, 'latest', 2, '', {
				academic_constants.ATT_CITATIONS,
				academic_constants.ATT_AUTHOR_AFFILIATION,
				academic_constants.ATT_WORDS,
				academic_constants.ATT_PAPER_TITLE,
				academic_constants.ATT_FIELD_OF_STUDY,
				academic_constants.ATT_YEAR,
				academic_constants.ATT_EXTENDED,
				academic_constants.ATT_ID,
				academic_constants.ATT_RERFENCES,
			})
			data = evaluate_request(params)

			# Authors papers
			if 'entities' in data:
				for paper in data['entities']:
					id = -1
					if ATT_ID in paper:
						id = paper[ATT_ID]

					p = AcademicPaper(paper[ATT_PAPER_TITLE].title(), id)

					if ATT_CITATIONS in paper:
						p.addCitations(paper[ATT_CITATIONS])

					if ATT_EXTENDED in paper:
						desc = json.dumps(paper[ATT_EXTENDED])
						try:
							desc = desc.split('\\"')
							if desc[5] == 'D':
								p.addDesc(desc[7])
								abKey = keySplit(parseQuery(desc[7]), cachedStopWords)
								p.addKeywords(abKey)
								score = jaccard_test(queryKeys, abKey)
								p.addScore(score)

							else:
								p.addDesc("none")
						except:
							print("No Abstract")
							break

					if ATT_YEAR in paper:
						p.year = paper[ATT_YEAR]
					author.addPaper(p)
			authors.append(author)
			cache.set(aId, author)
		else:
			# Cache hit
			authors.append(cachedAuthor)
			# Compute score
			cachedAuthor.score = 0  # Reset score
			for paper in cachedAuthor.papers:
				score = jaccard_test(queryKeys, paper.keywords)
				paper.addScore(score)
			print("Author= ", cachedAuthor.author_name)
	return authors


# 1
def compile_author_list(data):
	"""
	This is the first step of our query. Parses the a json response for authors and authorIds. Returning them in a dict
	:param data: json response from Evaluate request
	:return: a dict of authorIds mapped to author names
	"""
	authors = {}
	if 'entities' in data:
		for paper in data['entities']:
			# Iterate through paper authors and create Authors
			for auth in paper['AA']:
				auth_id = auth['AuId']
				auth_name = auth['AuN']
				if auth_id not in authors.keys():
					authors[auth_id] = auth_name
	else:
		# bad response
		print("Bad response")
	return authors


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
