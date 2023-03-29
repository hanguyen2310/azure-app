from django import forms
from .models import Content

class BlogForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["title", "genre", "author", "github_link", "body", "tag"]

    file_upload = forms.FileField(label='Or select a file (.md)', required=False)
    thumbnail = forms.ImageField(label='Select a thumbnail', required=False)
        

