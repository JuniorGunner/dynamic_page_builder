from django import forms
from .models import HTMLElement, WebPage


class HTMLElementForm(forms.ModelForm):
    class Meta:
        model = HTMLElement
        fields = ['tag_name', 'content', 'attributes', 'parent', 'page']


class WebPageForm(forms.ModelForm):
    class Meta:
        model = WebPage
        fields = ['name', 'slug']

