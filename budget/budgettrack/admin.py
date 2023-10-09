from django.contrib import admin
from .models import Account, Expense, Income, Transaction

admin.site.register(Account)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Transaction)