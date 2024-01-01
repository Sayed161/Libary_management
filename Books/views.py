from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .models import Books,review
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
class Details(DetailView):
    model = Books
    pk_url_kwarg = 'id'
    template_name = "details.html"

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data = self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
                new_comments = review_form.save(commit=False)
                new_comments.books = book
                new_comments.user = request.user
                print(new_comments)
                new_comments.save()
    
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.reviews.all()
        review_form = forms.ReviewForm()

        
        context['reviews']=reviews
        context['review_form']=review_form
        return context
    