import datetime
import decimal

from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User

from .exceptions import InvalidCurrencyError


class Account(models.Model):
    """Class for storing financial data"""
    CURRENCY_CHOICES = (
        ('RUR', 'RUR'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='RUR')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    owner = models.ForeignKey('Client', on_delete=models.CASCADE,
                              related_name='accounts', null=True)


class Transaction(models.Model):
    """Stores the movements of money"""
    sender = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='outgoing')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='incoming')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.CharField(max_length=255)
    t_dttm = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-t_dttm']


class Client(User):
    """The model of a client with account info and priority level"""
    level = models.PositiveSmallIntegerField(validators=[
                                             MinValueValidator(1),
                                             MaxValueValidator(3)],
                                             default=1)

    def add_account(self, currency, balance):
        if currency not in ['RUR', 'USD', 'EUR']:
            raise InvalidCurrencyError()
        Account.objects.create(currency=currency, balance=balance, owner=self)

    def delete_account(self, account_no):
        Account.objects.filter(id=account_no).delete()

    def transfer(self, source_account, target_account, amount, comment):
        if source_account.id != target_account.id:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
        Transaction.objects.create(sender=source_account,
                                   receiver=target_account,
                                   amount=amount,
                                   comment=comment)


class Admin(User):
    """The model of an admin, who maintains the bank services"""
    access_level = models.PositiveSmallIntegerField(validators=[
                                                    MinValueValidator(1),
                                                    MaxValueValidator(3)],
                                                    default=1)
