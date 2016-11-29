# Author object file
from AS_RequestHandler import test_query
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

	def getPapers(self):
		ret = []
		for paper in self.papers:
			ret.append(paper.title)
		return ret

	def addPaper(self, paper):
		"""
		Adds an AcademicPaper to the papers list of this author
		:param paper: AcademicPaper
		"""
		self.papers.append(paper)
		self.paperTitles.append(paper.title)

	def readData(self, data):
		if 'entities' in data:
			results = data['entities']
		else:
			return
		# results = test_query()

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

	def scoreAuthor(self):
		for paper in self.papers:
			self.score += paper.score

class AcademicPaper:
	def __init__(self, paper_title):
		self.score = 0
		self.title = paper_title
		self.authors = []
		self.keywords = []
		self.year = -1

	def addKeywords(self, keywords_list):
		for k in keywords_list:
			self.keywords.append(k)

	def addScore(self, score):
		self.score = score

	def addCitations(self, citations):
		self.citations = citations

	def addAuthor(self, author):
		self.authors.append(author)

	def addAuthors(self, author_list):
		"""
		:param author_list: list of AuId
		:return:
		"""
		for a in author_list:
			self.append(a)
