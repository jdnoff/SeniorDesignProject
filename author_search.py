import academic_constants
from topic_search import do_topic_search
from Author import *
from topic_search import score_authors
import academic_db_interface

# return authors papers to user for subset
# grab referenced papers and use them as initial search
#
# return all results

INITIAL_PAPER_QUERY = 20


def get_author_papers(authorName):
	"""
	Gets a list of an authors papers
	:param authorName: Name of the author
	:return: A list of papers by the given author
	"""
	query_string = "Composite(AA.AuN=\'{}\')".format(authorName)
	return academic_db_interface.get_papers(query_string, INITIAL_PAPER_QUERY)


def get_papers_by_id(paperIds):
	"""
	Gets a list of papers from paperids
	:param paperIds: List of paperids corresponding to selected papers
	:return: Populated list of papers
	"""
	# Make query
	wordslist = []
	count = 0
	for p in paperIds:
		wordslist.append("{}={}".format(academic_constants.ATT_ID, p))
		count += 1
	query_string = 'Or({})'.format(','.join(wordslist))
	return academic_db_interface.get_papers(query_string, count)


def search_papers(papers):
	"""
	This is the logic of author search. Performs an author search on the list of papers
	:param papers: List of papers to be searched
	:return: A populated list of authors ready to be displayed
	"""
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
