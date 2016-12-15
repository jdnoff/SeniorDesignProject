from academic_constants import *
from Author import Author, AcademicPaper
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from django.core.cache import cache
import json

attributes = {
	ATT_CITATIONS,
	ATT_AUTHOR_AFFILIATION,
	ATT_WORDS,
	ATT_PAPER_TITLE,
	ATT_FIELD_OF_STUDY,
	ATT_YEAR,
	ATT_CONFERENCE_NAME,
	ATT_JOURNAL_NAME,
	ATT_EXTENDED,
	ATT_ID,
	ATT_RERFENCES
}

attributes2 = {
	ATT_AUTHOR_NAME,
	ATT_AUTHOR_ID,
	ATT_WORDS,
	ATT_PAPER_TITLE,
	ATT_CITATIONS
}

def get_papers(query, numPapers):
	"""
	Gets papers from microsoft with a given query
	:param query: Query formatted for MAG
	:param numPapers: Number of papers to return
	:return: Populated list of papers
	"""
	params = construct_params(query, 'latest', numPapers, '', attributes)
	data = evaluate_request(params)
	paper_list = []
	if 'entities' in data:
		for paper in data['entities']:
			paper_id = -1
			if ATT_ID in paper:
				paper_id = paper[ATT_ID]

			p = AcademicPaper(paper[ATT_PAPER_TITLE].title(), paper_id)
			if ATT_WORDS in paper:
				p.addKeywords(paper[ATT_WORDS])

			if ATT_CITATIONS in paper:
				p.citations = paper[ATT_CITATIONS]

			if ATT_YEAR in paper:
				p.year = paper[ATT_YEAR]

			if ATT_RERFENCES in paper:
				p.addReferenceIds(paper[ATT_RERFENCES])

			if ATT_ID in paper:
				p.id = paper[ATT_ID]

			if ATT_EXTENDED in paper:
				desc = json.loads(paper[ATT_EXTENDED])

				if ATT_EXT_DESCRIPTION in desc:
					p.addDesc(desc[ATT_EXT_DESCRIPTION])
				else:
					p.addDesc("none")
					print("No abstract found for ", p.title)
			paper_list.append(p)

	return paper_list


def get_authors(query, numPapers, papers_per_author):
	"""
	Searches for papers using query and returns a populated list of authors of those papers
	:param query: Query string formatted for microsoft
	:param numPapers: Number of papers to search for
	:param papers_per_author: Number of papers to retrieve from each author
	:return: A populated list of authors
	"""

	params = construct_params(query, '', numPapers, '', attributes2)
	real_data = evaluate_request(params)

	# Get Author information
	authorId_list = compile_author_list(real_data)
	return get_list_of_authors(authorId_list, papers_per_author)


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


def get_list_of_authors(author_list, num_papers):
	"""
	Used to get additional information for a list of authors. Checks if an author is cached, if not it performs an
	evaluate request to get the information and caches it.
	:param author_list: a dict of author names to be searched
	:param num_papers: Number of papers to query per author
	:return: a list of Author objects
	"""
	authors = []
	for aId in author_list.keys():
		# Check cache
		cachedAuthor = cache.get(aId)
		if not cachedAuthor:
			# Cache miss
			# TODO: replace prints with logger
			print(author_list[aId], " Not in cache, searching microsoft")
			author = Author(author_list[aId], aId)
			query = "Composite({}={})".format(ATT_AUTHOR_ID, aId)
			params = construct_params(query, 'latest', num_papers, '', {
				ATT_CITATIONS,
				ATT_AUTHOR_AFFILIATION,
				ATT_WORDS,
				ATT_PAPER_TITLE,
				ATT_FIELD_OF_STUDY,
				ATT_YEAR,
				ATT_CONFERENCE_NAME,
				ATT_JOURNAL_NAME,
				ATT_EXTENDED,
				ATT_ID,
				ATT_RERFENCES,
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


