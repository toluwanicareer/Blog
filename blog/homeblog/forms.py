from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from .models import Post
from django import forms
from tinymce.widgets import TinyMCE


class SearchForm(forms.Form):
    query = forms.CharField()

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class TinyMCEWidget(TinyMCE): 
	def use_required_attribute(self, *args): 
		return False


class PostForm(forms.ModelForm): 
	body = forms.CharField( 
		widget=TinyMCEWidget( 
			attrs={'required': False, 'cols': 30, 'rows': 10} 
		) 
	) 
	class Meta: 
		model = Post 
		exclude = ("id", "slug")