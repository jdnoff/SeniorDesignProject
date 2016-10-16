from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View
from AS_RequestHandler import test_query
from .forms import TopicSearchForm
from .forms import AuthorSearchForm
from .forms import AuthorSearchSubsetForm


# Create your views here.
class LandingView(TemplateView):
	template_name = 'landing_page.html'


class TopicSearchView(View):
	form_class = TopicSearchForm
	template_name = 'search.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			# <process form cleaned data>
			data = form.cleaned_data
			return HttpResponseRedirect('/results/')

		return render(request, self.template_name, {'form': form})


class AuthorSearchView(View):
	form_class = AuthorSearchForm
	template_name = 'author_search.html'
	search_tmp = 'search.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.search_tmp, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			# <process form cleaned data>
			data = form.cleaned_data
			return render(request, self.template_name, {'form': AuthorSearchSubsetForm()})

		return render(request, self.search_tmp, {'form': form})


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
