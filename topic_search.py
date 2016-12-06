import json
from AS_RequestHandler import construct_params, evaluate_request
from Query_Parser import parseQuery
import academic_constants
from Author import *
from similarity_measure import cosine_sim
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
	# Initial AS Query
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, '', '10', '', attributes)
	real_data = evaluate_request(params)

	# Get Author information
	authorId_list = compile_author_list(real_data)
	populated_authors = search_list_of_authors(authorId_list)
	# Reset author scores
	for author in populated_authors:
		for p in author.papers:
			p.cosine_similarity = 0

	score_authors(populated_authors, abstract=abstract)

	# Compute scores for each author before sending them to be displayed
	for author in populated_authors:
		author.sumCitations()
		author.computeMostRecentYear()
		for p in author.papers:
			if p.title == p.desc:
				p.desc = "Not available"
		author.papers.sort(key=lambda paper: paper.cosine_similarity, reverse=True)

	populated_authors.sort(key=lambda author: author.cumulativeScore, reverse=True)
	return populated_authors


def score_authors(author_list, abstract):
	# NEW: create corpus from query words
	docs = {}
	cachedStopWords = stopwords.words("english")
	query = TextBlob(abstract.lower())
	docs[-1] = query
	corpWords = []
	for word in query.words:
		if word not in cachedStopWords and word not in corpWords:
			corpWords.append(word)
	# NEW: construct tf-idf vectors from documents
	maxCitations = 0
	for author in author_list:
		for paper in author.papers:
			if paper.citations > maxCitations:
				maxCitations = paper.citations
			if paper.id not in docs.keys():
				docs[paper.id] = TextBlob(paper.desc.lower())
	corpus = Corpus(docs, corpWords)
	corpus.constructVectors()

	# NEW: cosine similarity
	query = corpus.scoredDocs[0].vector  # <------- we dont really need this

	# original doc has id of -1
	for doc in corpus.scoredDocs:
		if doc.id == -1:
			query = doc.vector
	docDict = {}
	for document in corpus.scoredDocs:
		sim = cosine_sim(query, document.vector)
		document.addScore(sim)
		docDict[document.id] = sim

	for author in author_list:
		author.setCosineSimilarity(docDict)
		author.scoreAuthor(maxCitations)

# 2
def search_list_of_authors(author_list):
	"""
	Used to get additional information for a list of authors. Checks if an author is cached, if not it performs an
	evaluate request to get the information and caches it.
	:param author_list: a list of author names to be searched
	:return: a list of Author objects
	"""
	authors = []
	for aId in author_list.keys():
		# Check cache
		cachedAuthor = cache.get(aId)
		if not cachedAuthor:
			# Cache miss
			print(author_list[aId], " Not in cache, searching microsoft")
			author = Author(author_list[aId], aId)
			query = "Composite({}={})".format(academic_constants.ATT_AUTHOR_ID, aId)
			params = construct_params(query, 'latest', 30, '', {
				academic_constants.ATT_CITATIONS,
				academic_constants.ATT_AUTHOR_AFFILIATION,
				academic_constants.ATT_WORDS,
				academic_constants.ATT_PAPER_TITLE,
				academic_constants.ATT_FIELD_OF_STUDY,
				academic_constants.ATT_YEAR,
				academic_constants.ATT_CONFERENCE_NAME,
				academic_constants.ATT_JOURNAL_NAME,
				academic_constants.ATT_EXTENDED,
				academic_constants.ATT_ID,
				academic_constants.ATT_RERFENCES,
			})
			data = evaluate_request(params)

			# Authors papers
			if 'entities' in data:
				for paper in data['entities']:
					paper_id = -1
					if ATT_ID in paper:
						paper_id = paper[ATT_ID]

					p = AcademicPaper(paper[ATT_PAPER_TITLE].title(), paper_id)

					if 'C' in paper:
						if 'CN' in paper['C']:
							p.conference_name = paper['C']['CN'].upper()
							p.conference_name += ', '

					if 'J' in paper:
						if 'JN' in paper['J']:
							p.journal_name = paper['J']['JN'].upper()
							p.journal_name += ', '

					if ATT_CITATIONS in paper:
						p.citations = paper[ATT_CITATIONS]

					if ATT_EXTENDED in paper:
						desc = json.loads(paper[ATT_EXTENDED])

						if ATT_EXT_DESCRIPTION in desc:
							p.addDesc(desc[ATT_EXT_DESCRIPTION])
						else:
							p.addDesc(p.title)
							# print("No abstract found for ", p.title)
					if ATT_YEAR in paper:
						p.year = paper[ATT_YEAR]
					author.addPaper(p)
			authors.append(author)
			cache.set(aId, author)
		else:
			# Cache hit
			authors.append(cachedAuthor)
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
