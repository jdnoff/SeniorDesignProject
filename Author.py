# Author object file
from academic_constants import *


class Author:
	# List of Class Attributes:
	# author_name -- name of the author
	# author_id -- Microsoft Academic ID number of the author
	# papers -- list containing the Academic Paper objects of an author's papers
	# paperTitles -- list of the titles of an author's papers
	# citations -- total citations an author has across all papers
	# mostRecentYear -- the year of the author's most recent paper
	# cumulativeScore -- the final score given to an author based on their paper scores
	# coAuthorFlag -- A boolean value used in author search that indicates if the author
	#				  co-authored one of the input papers.

	def __init__(self, author_name, author_id):
		"""
		Initializes an author object, storing the author's name and id as attributes
		:param: author_name: name of the author.
				author_id: Microsoft Academic ID number of the author.
		:return: No return value.
		"""
		self.author_name = author_name.title()
		self.author_id = author_id

		self.papers = []
		self.paperTitles = self.getPapers()
		self.citations = 0
		self.mostRecentYear = -1
		self.numPublications = 0
		self.cumulativeScore = 0
		self.coAuthorFlag = False

	def computeMostRecentYear(self):
		"""
		Gets the most recent year that the author has published a paper in
		:param: No parameters. Uses self.papers attribute.
		:return: No return value.
		"""
		for paper in self.papers:
			if paper.year > self.mostRecentYear:
				self.mostRecentYear = paper.year

	def getPapers(self):
		"""
		Gets the titles of all an author's paper.
		:param: No parameters. Uses self.papers attribute.
		:return: ret: list of all paper titles.
		"""
		ret = []
		for paper in self.papers:
			ret.append(paper.title)
		return ret

	def setCosineSimilarity(self, docDict):
		"""
		Adds Cosine Similarity scores to each paper of this author
		:param docDict: Dict of paper ids mapped to scores
		:return: No return value.
		"""
		for paper in self.papers:
			if paper.id in docDict:
				paper.cosine_similarity += docDict[paper.id]

	def addPaper(self, paper):
		"""
		Adds an AcademicPaper to the papers list of this author
		:param paper: AcademicPaper
		"""
		self.papers.append(paper)
		self.paperTitles.append(paper.title)
		self.numPublications += 1

	def sumCitations(self):
		"""
		Sums the citations of all of an Author's papers and stores the value as an object
		attribute which represents the total citations an author has.
		:param No parameters. Uses self.papers attribute.
		:return: No return value.
		"""
		for paper in self.papers:
			self.citations += paper.citations

	def scorePapers(self, maxCitations):
		"""
		Scores each paper an Author has.
		:param No parameters. Uses self.papers attribute.
		:return: No return value.
		"""
		for paper in self.papers:
			paper.scorePaper(maxCitations)

	def scoreAuthor(self):
		"""
		Scores each an Author based on the average of their 10 highest document scores.
		Stores the value as an object attribute.
		:param No parameters. Uses self.papers attribute.
		:return: No return value.
		"""
		total = 0
		for paper in self.papers[:10]:
			total += paper.finalScore
		self.cumulativeScore = total/len(self.papers[:10])

class AcademicPaper:
	# List of Class Attributes:
	# id -- ID number of the paper.
	# cosine_similarity -- cosine similarity score of a paper compared to the user's input.
	# title -- the title of the paper.
	# citations -- number of citations the paper has.
	# year -- the year the paper was published in.
	# finalScore -- the final score given to the paper based on similarity, citations, and year.
	# authors -- list of author's who contributed to the paper.
	# desc -- text of the paper's abstract
	# journal_name -- name of the journal the paper appeared in (if applicable)
	# conference_name -- name of the conference the paper appeared in (if applicable)

	def __init__(self, paper_title, id):
		"""
		Initializes a paper object, storing the papers title and id as attributes
		:param: paper_title: title of the paper.
				id: ID number of the paper.
		:return: No return value.
		"""
		self.id = id
		self.cosine_similarity = 0
		self.title = paper_title
		self.authors = []
		self.year = -1
		self.desc = ""
		self.journal_name = ""
		self.conference_name = ""
		self.citations = 0
		self.finalScore = 0

	def addDesc(self, desc):
		"""
		Adds an abstract to the paper object.
		:param: desc: the abstract of the paper
		:return: No return value.
		"""
		self.desc = desc

	def addAuthor(self, author):
		"""
		Adds an author to the paper object.
		:param: author: the name of the author who contributed to the paper
		:return: No return value.
		"""
		self.authors.append(author)

	def scorePaper(self, maxCitations):
		"""
		Gives the paper a weighted score based on its Similarity, citations, and recency.
		citations is put over the max citations and year put over 2016 to put both metrics
		on a 0-1 scale so they can be weighted accurately.
		:param: maxCitations: Maximum number of citations for papers across all authors.
		:return: No return value.
		"""
		self.finalScore = ( (.75)*(self.cosine_similarity) + (.2)*(self.citations/maxCitations) + (.05)*(self.year/2016) )

