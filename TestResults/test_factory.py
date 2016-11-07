import json
import os


def get_test_results(filename):
	cur_path = os.path.dirname(__file__)
	new_path = os.path.relpath(filename, cur_path)

	with open('{}\\{}'.format(cur_path, filename), 'r') as data_file:
		return json.load(data_file)


def get_evaluate_test_results():
	return get_test_results("evaluate_results_25.txt")
