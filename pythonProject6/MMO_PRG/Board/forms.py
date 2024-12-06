from ckeditor.fields import RichTextField
from django import forms
from .models import Ad, Response, NewsletterSubscription


class AdForm(forms.ModelForm):
    content = RichTextField

    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'content']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']