from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from django.views.generic.list import ListView

from AS_RequestHandler import query
from AS_RequestHandler import test_query

from .forms import TopicSearchForm
from .forms import AuthorSearchForm
from .forms import AuthorSearchSubsetForm

# Create your views here.


def landing_page(request):
	return render(request, 'landing_page.html')


def author_search(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = AuthorSearchForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return render(request, 'search.html', {'form': AuthorSearchSubsetForm()})

		# if a GET (or any other method) we'll create a blank form
	else:
		form = AuthorSearchForm()

	return render(request, 'search.html', {'form': form})


def topic_search(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TopicSearchForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

		# if a GET (or any other method) we'll create a blank form
	else:
		form = TopicSearchForm()

	return render(request, 'search.html', {'form': form})


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
