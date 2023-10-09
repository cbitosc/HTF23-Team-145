from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

class CustomUser(AbstractUser):
    # Your custom user fields here, if any
    pass

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.account_name

    def calculate_total_expenses(self):
        total_expenses = Expense.objects.filter(account=self).aggregate(total_expenses=Sum('amount'))['total_expenses']
        return total_expenses or 0

    def calculate_total_income(self):
        total_income = Income.objects.filter(account=self).aggregate(total_income=Sum('amount'))['total_income']
        return total_income or 0

    def transfer_in(self):
        transferin = Transaction.objects.filter(receiver_account=self).aggregate(total_income=Sum('amount'))['total_income']
        return transferin or 0

    def transfer_out(self):
        transferout = Transaction.objects.filter(sender_account=self).aggregate(total_income=Sum('amount'))['total_income']
        return transferout or 0

    def calculate_current_balance(self):
        total_expenses = self.calculate_total_expenses()
        total_income = self.calculate_total_income()
        transferout = self.transfer_out()
        transferin = self.transfer_in()
        return self.original_amount + total_income - total_expenses - transferout + transferin

class Expense(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note_or_description = models.TextField()

    def __str__(self):
        return self.name

class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note_or_description = models.TextField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction: {self.sender_account} to {self.receiver_account}"



