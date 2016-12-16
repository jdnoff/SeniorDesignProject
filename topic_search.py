from Query_Parser import parseQuery
import academic_constants
from Author import *
from similarity_measure import cosine_sim
from nltk.corpus import stopwords
from Corpus import *
import academic_db_interface


"""
IMPORTANT: run this function and download stopwords corpus from the window:
				nltk.download()
"""

# Size parameters for each query
QUERY_SIZE_INITIAL = 13
QUERY_SIZE_AUTHOR = 40

# Handler for the topic search use case
def do_topic_search(abstract):
	"""
	Handler for the topic search use case
	:param abstract: full text of a paper abstract
	:return: List of Authors ready to be displayed
	"""
	# Initial AS Query
	keyword_list = parseQuery(abstract)
	query_string = create_query(keyword_list)
	populated_authors = academic_db_interface.get_authors(query_string, QUERY_SIZE_INITIAL, QUERY_SIZE_AUTHOR)

	# Reset author scores to 0
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
	populated_authors = list(filter(lambda a: a.numPublications > 3, populated_authors))
	populated_authors.sort(key=lambda author: author.cumulativeScore, reverse=True)
	return populated_authors


def score_authors(author_list, abstract):
	"""
	Scores a list of authors against a given abstract
	:param author_list: A list of authors populated with papers
	:param abstract: Abstract to be scored against
	:return:
	"""
	# create corpus from query words
	docs = {}
	cachedStopWords = stopwords.words("english")
	query = TextBlob(abstract.lower())
	docs[-1] = query
	corpWords = []
	for word in query.words:
		if word not in cachedStopWords and word not in corpWords:
			corpWords.append(word)
	# construct tf-idf vectors from documents
	maxCitations = 0
	for author in author_list:
		for paper in author.papers:
			if paper.citations > maxCitations:
				maxCitations = paper.citations
			if paper.id not in docs.keys():
				docs[paper.id] = TextBlob(paper.desc.lower())
	corpus = Corpus(docs, corpWords)
	corpus.constructVectors()

	# cosine similarity
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

	for author in author_list:
		author.setCosineSimilarity(docDict)
		author.scorePapers(maxCitations)
		author.papers.sort(key=lambda paper: paper.finalScore, reverse=True)
		author.scoreAuthor()


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
