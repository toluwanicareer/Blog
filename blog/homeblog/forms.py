from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from .models import Post, Comment
from django import forms
from tinymce.widgets import TinyMCE



# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

# class NewPostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super(NewPostForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })


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
		fields = '__all__'
