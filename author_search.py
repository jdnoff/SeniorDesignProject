import academic_constants
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from topic_search import do_topic_search
from Author import *
import json


# return authors papers to user for subset
# grab referenced papers and use them as initial search
#
# return all results

def get_author_papers(authorName):
	attributes = {
		academic_constants.ATT_ID,
		academic_constants.ATT_AUTHOR_NAME,
		academic_constants.ATT_AUTHOR_ID,
		academic_constants.ATT_WORDS,
		academic_constants.ATT_PAPER_TITLE,
		academic_constants.ATT_CITATIONS,
		academic_constants.ATT_RERFENCES,
		academic_constants.ATT_EXTENDED
	}
	query_string = "Composite(AA.AuN=\'{}\')".format(authorName)
	params = construct_params(query_string, 'latest', '10', '', attributes)
	real_data = evaluate_request(params)
	print(json.dumps(real_data))
	return read_response(real_data)


def read_response(data):
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
				p.addCitations(paper[ATT_CITATIONS])

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
			print(p.title)
			paper_list.append(p)

	return paper_list


def search_paperids(paperIds):
	"""
	Performs a topic search on each paperid, returning a list of authors
	:param paperIds: A list of paper ids to be searched
	:return: a list of authors sorted and ready to be displayed
	"""
	# Make query
	attributes = {
		academic_constants.ATT_ID,
		academic_constants.ATT_AUTHOR_NAME,
		academic_constants.ATT_AUTHOR_ID,
		academic_constants.ATT_WORDS,
		academic_constants.ATT_PAPER_TITLE,
		academic_constants.ATT_CITATIONS,
		academic_constants.ATT_RERFENCES,
		academic_constants.ATT_EXTENDED
	}
	wordslist = []
	count = 0
	for p in paperIds:
		wordslist.append("{}={}".format(academic_constants.ATT_ID, p))
		count += 1
	query_string = 'Or({})'.format(','.join(wordslist))
	params = construct_params(query_string, 'latest', count, '', attributes)
	data = evaluate_request(params)
	papers = read_response(data)

	total_authors = []
	# Do topic search on each paper description
	for p in papers:
		print("Title", p.title, "\n", p.desc)
		if p.desc != "none":
			total_authors += do_topic_search(p.desc)
	total_authors.sort(key=lambda author: author.cumulativeScore, reverse=True)
	return total_authors
