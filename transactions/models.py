from django.db import models
from accounts.models import UserAccount
from Books.models import Books
from .constant import TRANSACTION_TYPE
# Create your models here.

class Transactions(models.Model):
    account = models.ForeignKey(UserAccount,related_name='transactions',on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Borrow_book(models.Model):
    user_account = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transactions_type = models.IntegerField(choices=TRANSACTION_TYPE,null = True)
    class Meta :
        ordering = ['timestamp']