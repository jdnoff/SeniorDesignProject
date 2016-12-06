# Author object file
from academic_constants import *


class Author:
	# List of Class Attributes
	# paperTitles -- list of all papers associated with this author given by the query (given by 'Ti' attribute)
	# keyWords -- list of all keywords from all papers in paperTitles (given by 'W' attribute)
	# fieldsOfStudy -- list of all fields of study the papers encompass (given by 'F.FN' attribute)
	# citationByPaper -- number of citations for each paper in result list (given by 'CC' attribute)
	# used to sum all total citations for an author

	def __init__(self, author_name, author_id):
		# input should be the json result of a query for an author
		self.author_name = author_name.title()
		self.author_id = author_id
		# which gets the attributes 'Ti', 'W', 'F.FN', 'CC'

		# Stores the raw ranking score
		self.score = 0
		self.papers = []
		self.paperTitles = self.getPapers()
		self.keyWords = []
		self.fieldsOfStudy = []
		self.citations = 0
		self.mostRecentYear = -1
		self.numPublications = 0
		self.cumulativeScore = 0

	def totalScore(self):
		self.cumulativeScore = (self.citations / 10000) + self.score

	def computeMostRecentYear(self):
		for paper in self.papers:
			if paper.year > self.mostRecentYear:
				self.mostRecentYear = paper.year

	def getPapers(self):
		ret = []
		for paper in self.papers:
			ret.append(paper.title)
		return ret

	def setCosineSimilarity(self, docDict):
		"""
		Adds tfidf similarity scores to each paper of this author
		:param docDict: Dict of paper ids mapped to scores
		:return:
		"""
		for paper in self.papers:
			if paper.id in docDict:
				paper.cosine_similarity = docDict[paper.id]

	def addPaper(self, paper):
		"""
		Adds an AcademicPaper to the papers list of this author
		:param paper: AcademicPaper
		"""
		self.papers.append(paper)
		self.paperTitles.append(paper.title)
		self.numPublications += 1

	def readData(self, data):
		if 'entities' in data:
			results = data['entities']
		else:
			return

		for paper in results:
			self.paperTitles.append(paper[ATT_PAPER_TITLE].title())
			self.citationByPaper.append(int(paper[ATT_CITATIONS]))
			if ATT_WORDS in paper:
				self.keyWords += (paper[ATT_WORDS])
			if 'F' in paper:
				for field in paper['F']:
					self.fieldsOfStudy.append(field['FN'])

	def sumCitations(self):
		for paper in self.papers:
			self.citations += paper.citations

	def scoreAuthor(self, maxCitations):
		total = 0
		for paper in self.papers:
			paper.finalScore =( (.8)*(paper.cosine_similarity) + (.15)*(paper.citations/maxCitations) + (.05)*(paper.year/2016) )
			total += paper.finalScore
		self.cumulativeScore = total

class AcademicPaper:
	def __init__(self, paper_title, id):
		self.id = id
		self.cosine_similarity = 0
		self.title = paper_title
		self.authors = []
		self.keywords = []
		self.year = -1
		self.desc = ""
		self.referenceIds = []
		self.journal_name = ""
		self.conference_name = ""
		self.citations = 0
		self.finalScore = 0

	def addReferenceIds(self, refIds):
		for ref in refIds:
			self.referenceIds.append(ref)

	def addKeywords(self, keywords_list):
		for k in keywords_list:
			self.keywords.append(k)

	def addDesc(self, desc):
		self.desc = desc

	def addAuthor(self, author):
		self.authors.append(author)

	def addAuthors(self, author_list):
		"""
		:param author_list: list of AuId
		:return:
		"""
		for a in author_list:
			self.append(a)
