from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import reverse
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View
from .forms import TopicSearchForm
from .forms import AuthorSearchForm
from .forms import AuthorSearchSubsetForm
from topic_search import do_topic_search
from author_search import get_author_papers
from author_search import search_paperids

# Create your views here.
class LandingView(TemplateView):
	template_name = 'landing_page.html'


class AboutUsView(TemplateView):
	template_name = 'about_us.html'


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

			author_list = do_topic_search(abstract)

			return render(request, 'results.html', {
				'results_list': author_list,
				'query': title
			})

		return render(request, self.template_name, {'form': form})


class AuthorSearchView(View):
	form_class = AuthorSearchForm
	template_name = 'subset_page.html'
	search_tmp = 'search.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.search_tmp, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		# Search subset of papers
		if 'subset' in request.POST:
			paperIds = request.POST.getlist('paper_list')
			author_list = search_paperids(paperIds)

			return render(request, 'results.html', {
				'results_list': author_list,
				'query': "test"
			})
		else:
			# get author name and body of work
			if form.is_valid():
				# <process form cleaned data>
				data = form.cleaned_data
				author = data['author']
				papers = get_author_papers(author)
				subsetForm = AuthorSearchSubsetForm()
				c = [(p.id, p.title) for p in papers]
				subsetForm.fields['paper_list'].choices = c
				return render(request, self.template_name, {'form': subsetForm})

		return render(request, self.search_tmp, {'form': form})
