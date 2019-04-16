import datetime

from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

LAST_CREATED_ACCOUNT_NO = 1000000


class User(models.Model):
    """Main User class"""
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    join_dt = models.DateField(default=timezone.now)
    quit_dt = models.DateField(default=datetime.date(2099, 1, 1))


class Account(models.Model):
    """Class for storing financial data"""
    def __init__(self):
        global LAST_CREATED_ACCOUNT_NO
        LAST_CREATED_ACCOUNT_NO += 1

    CURRENCY_CHOICES = (
        ('rur', 'RUR'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='rur')
    account_no = models.IntegerField(default=LAST_CREATED_ACCOUNT_NO)
    balance = models.DecimalField(max_digits=15, decimal_places=2)


class TransactionHistory(models.Model):
    """Stores the movements of money"""
    sender = models.ForeignKey(Account, on_delete=models.PROTECT,
                               related_name='outgoing')
    receiver = models.ForeignKey(Account, on_delete=models.PROTECT,
                                 related_name='incoming')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.CharField(max_length=255)
    transaction_dttm = models.DateTimeField(default=timezone.now)


class Client(User):
    """The model of a client with account info and priority level"""
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='owner')
    level = models.PositiveSmallIntegerField(validators=[
                                             MinValueValidator(1),
                                             MaxValueValidator(3)],
                                             default=1)


class Admin(User):
    """The model of an admin, who maintains the bank services"""
    access_level = models.PositiveSmallIntegerField(validators=[
                                                    MinValueValidator(1),
                                                    MaxValueValidator(3)],
                                                    default=1)
