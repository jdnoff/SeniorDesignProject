from django.shortcuts import render

import json
from AS_RequestHandler import query
from AS_RequestHandler import test_query
from django.http import HttpResponse


# Create your views here.


def index(request):
	return render(request, 'search.html')


def search(request):
	if request.method == 'GET':
		search_query = request.GET.get('search_box', None)

		""" test_query returns a sample results list. Use this for testing instead of query so we can cut down on the
		number of requests sent to microsoft academic"""
		# results = query(search_query)
		results = test_query()

		# Send query to page for testing
		return render(request, 'results.html', {
			'query': search_query,
			'results_list': results
		})

	else:
		return render(request, 'styled_base.html')
