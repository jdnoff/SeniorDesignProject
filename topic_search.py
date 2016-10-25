from nltk.corpus import stopwords
from AS_RequestHandler import interpret_request
import string
import json
from AS_RequestHandler import construct_params
from AS_RequestHandler import evaluate_request
import academic_constants


# Handler for the topic search use case

def do_topic_search(abstract):
	attributes = {academic_constants.ATT_AUTHOR_NAME}
	# TODO: Send abstract to query processor
	keyword_list = get_keywords(abstract)
	query_string = create_query(keyword_list)
	params = construct_params(query_string, 'latest', '10', '', attributes)
	# TODO: Do evaluate request
	return


# Generate a query for AS
def get_keywords(paper_abstract):
	"""
	Creates a list of keywords from a given an abstract
	:param paper_abstract: Paper's full text abstract
	:return: a list of keywords
	"""
	stop = set(stopwords.words('english'))
	punct = set(string.punctuation)
	abstract_no_punct = ''.join(ch for ch in paper_abstract.lower() if ch not in punct)
	words = []
	for word in abstract_no_punct.split():
		if word not in stop:
			words.append(word)
	return words


# STUB
def create_query(keyword_list):
	return keyword_list


def test_get_keywords():
	abstract = """Social network services have become a viable source of information for users. In Twitter, information
				deemed important by the community propagates through retweets. Studying the characteristics of such
				popular messages is important for a number of tasks, such as breaking news detection, personalized
				message recommendation, viral marketing and others. This paper investigates the problem of predicting
				the popularity of messages as measured by the number of future retweets and sheds some light on what
				kinds of factors influence information propagation in Twitter. We formulate the task into a
				classification problem and study two of its variants by investigating a wide spectrum of features
				based on the content of the messages, temporal information, metadata of messages and users, as well as
				structural properties of the users' social graph on a large scale dataset. We show that our method can
				successfully predict messages which will attract thousands of retweets with good performance."""
	keys = get_keywords(abstract)
	print(json.dumps(interpret_request(' '.join(keys)), indent=4))


test_get_keywords()
