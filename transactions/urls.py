from django.urls import path,include
from .views import DepositMoneyView,BorrowingView,ReturnView,TransectionReportView
urlpatterns = [
    path('deposite/', DepositMoneyView.as_view(), name='deposite'),
    path('borrow/<int:book_id>', BorrowingView.as_view(), name='borrow'),
    path('return_book/<int:book_id>', ReturnView.as_view(), name='return_book'),
    path('report/', TransectionReportView.as_view(), name='report'),
]