import academic_constants
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
from topic_search import do_topic_search
from Author import *
import json
from topic_search import score_authors


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


def get_papers_by_id(paperIds):
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
	return read_response(data)


def search_papers(papers):
	total_authors = {}
	# Do topic search on each paper description
	for p in papers:
		if p.desc != "none":
			total_authors[p.id] = do_topic_search(p.desc)

	ret_list = []
	# Score similarity against other papers
	for key in total_authors.keys():
		for p in papers:
			if key != p.id:
				score_authors(total_authors[key], p.desc)
		for author in total_authors[key]:
			# if author not in ret_list:
			if not any(author.author_id == a.author_id for a in ret_list):
				# Add author
				ret_list.append(author)
			else:
				# Duplicate author
				for a in ret_list:
					if a.author_id == author.author_id:
						dd = {}
						for p in author.papers:
							dd[p.id] = p.cosine_similarity
						a.setCosineSimilarity(dd)
	ret_list.sort(key=lambda author: author.cumulativeScore, reverse=True)
	# Detect co-authorship
	paper_set = set([p.id for p in papers])
	for author in ret_list:
		author.coAuthorFlag = len(paper_set.intersection(set([p.id for p in author.papers]))) > 0
	return ret_list
