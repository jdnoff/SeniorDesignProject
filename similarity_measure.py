# file which contains all functions for measuring
# similarity between documents

from Query_Parser import *
import fileinput
from textblob import TextBlob
import math

def term_freq(word, doc):
	return doc.words.count(word)/len(doc.words)

def n_containing(word, docList):
	return sum(1 for doc in docList if word in doc.words)

def inverse_doc_freq(word, docList):
	return math.log(len(docList) / (1+n_containing(word, docList)))

def tf_idf(word, doc, docList):
	return term_freq(word, doc) * inverse_doc_freq(word, docList)

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

def keySplit(doc, cachedStopWords):
	wordList = []
	for term in doc:
		list = term.split(" ")
		for word in list:
			if word not in cachedStopWords:
				wordList.append(word)
	return wordList

def jaccard_test(doc_one, doc_two):
	union = set(doc_one).union(doc_two)
	intersect = set(doc_one).intersection(doc_two)
	index = len(intersect) / len(union)
	return index
