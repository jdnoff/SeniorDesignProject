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

	def __init__(self, author_name, author_id, data):
		# input should be the json result of a query for an author
		self.author_name = author_name
		self.author_id = author_id
		# which gets the attributes 'Ti', 'W', 'F.FN', 'CC'
		results = []
		if 'entities' in data:
			results = data['entities']
		else:
			return
		# results = test_query()

		self.paperTitles = []
		self.keyWords = []
		self.fieldsOfStudy = []
		self.citationByPaper = []
		for paper in results:
			self.paperTitles.append(paper[ATT_PAPER_TITLE].title())
			self.citationByPaper.append(int(paper[ATT_CITATIONS]))
			if ATT_WORDS in paper:
				self.keyWords += (paper[ATT_WORDS])
			if 'F' in paper:
				for field in paper['F']:
					self.fieldsOfStudy.append(field['FN'])
		self.totalCitations = self.sumCitations()

	def sumCitations(self):
		total = 0
		for i in self.citationByPaper:
			total += i
		return total
