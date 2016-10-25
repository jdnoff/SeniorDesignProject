from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View
from AS_RequestHandler import test_query
from .forms import TopicSearchForm
from .forms import AuthorSearchForm
from .forms import AuthorSearchSubsetForm
from topic_search import do_topic_search

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
			title = data['manuscript_title']
			author = data['manuscript_author']
			abstract = data['manuscript_abstract']
			# TODO: generate query from this data and send query to academic search
			do_topic_search(abstract)

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
			author = data['author']
			# TODO: Search author in AS then display paper results in next form

			return render(request, self.template_name, {'form': AuthorSearchSubsetForm()})

		return render(request, self.search_tmp, {'form': form})


class ResultsView(TemplateView):
	template_name = 'results.html'

	def get_context_data(self, **kwargs):
		context = {
			'results_list': test_query(),
			'query': "Test Query"
		}
		return context
