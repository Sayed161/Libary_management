from django import forms
from .models import Books,review

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = review
        fields  = ['star']
