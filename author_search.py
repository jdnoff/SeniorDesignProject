import academic_constants
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from Author import *
import json


def do_author_search(authorName):
	# Search authors papers
	print("hi")


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
		academic_constants.ATT_RERFENCES
	}
	query_string = "Composite(AA.AuN=\'{}\')".format(authorName)
	params = construct_params(query_string, 'latest', '5', '', attributes)
	real_data = evaluate_request(params)
	print(json.dumps(real_data))
	paper_list = []
	if 'entities' in real_data:
		for paper in real_data['entities']:
			p = AcademicPaper(paper[ATT_PAPER_TITLE].title())
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
			print(p.title)
			paper_list.append(p)

	return paper_list
