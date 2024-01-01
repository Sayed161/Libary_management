from django.urls import path,include
from .views import userRegistrationview,UserLoginView,LogOut,profile
urlpatterns = [
    path('register/', userRegistrationview.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', LogOut,name='logout'),
    path('profile/', profile.as_view(),name='profile'),
]
