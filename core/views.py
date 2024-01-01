from typing import Any
from django.http import HttpRequest
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView
from category.models import catagory
from Books.models import Books

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request,catagory_slug=None):
        data = Books.objects.all()
        if catagory_slug is not None:
            category = catagory.objects.get(slug=catagory_slug)
            data = Books.objects.filter(category=category)
        categories = catagory.objects.all()
        return self.render_to_response({'data': data, 'category': categories})