# file which contains all functions for measuring
# similarity between documents

from Query_Parser import *
import fileinput
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
import academic_constants


def get_corpus():
	words = []
	for line in fileinput.input('Corpus.txt'):
		l = line[0: len(line) - 1]
		s = l.split(" ")
		for word in s:
			words.append(word)
	return words


def get_corpus_phrases():
	phrases = []
	for line in fileinput.input('Corpus_phrases.txt'):
		l = line[0: len(line) - 1]
		phrases.append(l)
	print(phrases)
	return phrases


def in_corpus(key):
	corpus = get_corpus()
	for word in corpus:
		if key == word:
			return True
	return False


def in_phrases(key):
	corpus = get_corpus_phrases()
	for phrase in corpus:
		if key == phrase:
			return True
	return False


def jaccard_test():
	doc_one = test_query()
	doc_one = doc_one['documents'][0]['keyPhrases']
	doc_two = ['data mining technology', 'complex data', 'data warehouses', 'mining stream', 'live data', 'real-world',
	           'guide', 'theory', 'practice']
	union = set(doc_one).union(doc_two)
	intersect = set(doc_one).intersection(doc_two)
	index = len(intersect) / len(union)
	print(index)
