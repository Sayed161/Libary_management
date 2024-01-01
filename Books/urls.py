from django.urls import path,include
from .views import Details
urlpatterns = [
    path('details/<int:id>', Details.as_view(), name='details'),
]