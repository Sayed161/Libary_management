# Generated by Django 4.2.7 on 2024-01-01 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_borrow_book_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow_book',
            name='transaction',
        ),
    ]
