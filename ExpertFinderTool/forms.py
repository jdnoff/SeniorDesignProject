from django import forms

style_attribute = {'class': 'w3-input w3-border w3-padding'}
test_paper_list = ['paper 1', 'paper 2', 'paper 3', 'paper 4', 'paper 5', 'paper 6', 'paper 7']


class TopicSearchForm(forms.Form):
	manuscript_title = forms.CharField(label='Manuscript Title', max_length=200, required=False,
	                                   widget=forms.TextInput(attrs=style_attribute))
	manuscript_abstract = forms.CharField(label='Manuscript Abstract', max_length=3000, required=True,
	                                      widget=forms.Textarea(attrs=style_attribute))


class AuthorSearchForm(forms.Form):
	author = forms.CharField(label='Author Name', max_length=1000, required=False,
	                         widget=forms.TextInput(attrs=style_attribute))


class AuthorSearchSubsetForm(forms.Form):
	paper_list = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs=
	                                                                           {'class': 'w3-check',
	                                                                            'style': 'list-style-type: none'
	                                                                            }), label='')
