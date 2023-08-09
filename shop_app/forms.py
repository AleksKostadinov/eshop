from django import forms
from django.core import validators

from shop_app.models import ReviewRating


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}
            ))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
            ))
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Subject'}
            ))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Enter your message'}
            ))
    botcatcher = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        validators=[validators.MaxLengthValidator(0)]
            )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ('subject', 'review', 'rating',)
