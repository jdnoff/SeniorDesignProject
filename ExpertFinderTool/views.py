from django.shortcuts import render

import json
from AS_RequestHandler import query
from django.http import HttpResponse
# Create your views here.


test_sq = "hello"
test_context = {'query': test_sq, 'results_list': test_results_list}


def index(request):
    return render(request, 'search.html')


def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)

        results = query(search_query)
        context = {'query': search_query, 'results_list': results}

        # Send query to page for testing
        return render(request, 'results.html', context)
