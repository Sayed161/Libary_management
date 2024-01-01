from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,ListView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Sum
from django.urls import reverse_lazy
from Books.models import Books
from . models import Borrow_book
from . constant import BORROW,RETURN


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class DepositMoneyView(FormView):
    form_class = DepositForm
    title = "Deposite"
    template_name = "deposite.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        account = self.request.user.accounts
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request,f"{amount}$ was deposited to your account successfully")
        send_transaction_email(self.request.user, amount, "Deposite Message", "deposite_mail.html")
        return super().form_valid(form)
    
    def get_form_kwargs(self) :
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.accounts,     
        })
        return kwargs
    

class BorrowingView(LoginRequiredMixin,View):
    def get(self, request, book_id):
        books = get_object_or_404(Books,id = book_id)
        print(books)
        if not books.is_borrowed :
            account = self.request.user.accounts
            if books.borrowing_price < account.balance :
                account.balance -= books.borrowing_price
                account.balance_after_transaction = account.balance
                account.transactions_type = BORROW
                account.save()

                books.is_borrowed = True
                books.save()


                Borrow_book.objects.create(
                    user_account=account,
                    book=books,
                    transactions_type=BORROW,
                    timestamp=datetime.now(),
                )
                return redirect ("report")
            else:
                messages.error(self.request,f"You don't have enough money to pay the loan")
                return redirect("home")
            
class ReturnView(LoginRequiredMixin,View):
    def get(self, request, book_id):
        books = get_object_or_404(Books,id = book_id)
        if books.is_borrowed :
            account = self.request.user.accounts
            if books.borrowing_price < account.balance :
                account.balance += books.borrowing_price
                account.balance_after_transaction = account.balance
                account.transactions_type = RETURN
                account.save()

                books.is_borrowed = False
                books.save()

                Borrow_book.objects.create(
                    user_account=account,
                    book=books,
                    transactions_type=RETURN,
                    timestamp=datetime.now(),
                )


                return redirect ("report")
            else:
                messages.error(self.request,f"You don't have enough money to pay the loan")
                return redirect("home")



class TransectionReportView(LoginRequiredMixin,ListView):
    template_name = "transaction_report.html"
    model = Borrow_book

    def get_queryset(self):
        # queryset = Borrow_book.objects.filter(user_account  = self.request.user.accounts, transactions_type = BORROW)
        queryset = super().get_queryset().filter(
            user_account=self.request.user.accounts
        )
        print(queryset)
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str :
            start_date = datetime.strptime(start_date_str,"%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str,"%Y-%m-%d").date()
            queryset = queryset.filter(timestamp__date__gte = start_date,timestamp__date__lte = end_date )
        
        
        return queryset.distinct()
    