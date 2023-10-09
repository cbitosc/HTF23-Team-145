from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.urls import reverse

from .models import CustomUser, Account, Expense, Income, Transaction

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['type'] == 'account':
                name = request.POST['accountName']
                amount = request.POST['originalAmount']
                user = request.user
                newaccount = Account(user = user, account_name = name, original_amount = amount)
                newaccount.save()
            elif request.POST['type'] == 'expense':
                name = request.POST['title']
                account = Account.objects.get(user = request.user,account_name = request.POST['account'])
                amount = request.POST['amount']
                note = request.POST['entryDescription']
                newExpense = Expense(account=account, name = name, amount = amount, note_or_description=note)
                newExpense.save()
                account.calculate_current_balance()
            elif request.POST['type'] == 'income':
                name = request.POST['title']
                account = Account.objects.get(user = request.user,account_name = request.POST['account'])
                amount = request.POST['amount']
                note = request.POST['entryDescription']
                newExpense = Income(account=account, name = name, amount = amount, note_or_description=note)
                newExpense.save()
                account.calculate_current_balance()
            elif request.POST['type'] == 'transaction':
                title = request.POST['title']
                fromacc = Account.objects.get(user = request.user,account_name = request.POST['fromAccount'])
                toacc = Account.objects.get(user = request.user,account_name = request.POST['toAccount'])
                amount = int(request.POST['amount'])
                newTransfer = Transaction(name = title, sender_account = fromacc, receiver_account=toacc, amount = amount)
                newTransfer.save()
                fromacc.calculate_current_balance()
                toacc.calculate_current_balance()               

        user = request.user
        user_accounts = Account.objects.filter(user=user)
        expenses = []
        incomes = []
        transactions = []
        for account in user_accounts:
            expense = Expense.objects.filter(account = account)
            income = Income.objects.filter(account = account)
            transaction = Transaction.objects.filter(sender_account = account)
            t = Transaction.objects.filter(receiver_account = account)
            expenses += expense
            incomes+= income
            transactions += t
            transactions += transaction  
        transactions = set(transactions)      

        return render(request, 'budgettrack/index.html', {
            'accounts':user_accounts,
            'expenses':expenses,
            'incomes': incomes,
            'transactions':transactions
        })
    else:
        return render(request, 'budgettrack/login.html')

def delacc(request, acc):
    account = Account.objects.get(user = request.user, account_name = acc)
    account.delete()
    return HttpResponseRedirect(reverse('index'))

def delpage(request, type, name):
    if type=='income':
        record = Income.objects.get(name = name)
        record.delete()
        return HttpResponseRedirect(reverse('index'))
    elif type=='expense':
        record = Expense.objects.get(name = name)
        record.delete()
        return HttpResponseRedirect(reverse('index'))
    elif type == 'transfer':
        record = Transaction.objects.get(name = name)
        record.delete()
        return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'budgettrack/login.html', {
                'message':'invalid credentials'
            })
    return render(request, 'budgettrack/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'budgettrack/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1!= password2:
            return render(request, 'budgettrack/register.html',{
                'message':'please make sure the passwords match'
            })
        email = request.POST['email']

        try:
            user = CustomUser.objects.create_user(username=username, password=password1, email=email)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "budgettrack/register.html", {
                "message": "Email address already taken."
            })
        # user = prof.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return render(request, 'budgettrack/index.html')  # Change 'dashboard' to your desired URL
    else:
        return render(request, 'budgettrack/register.html')

def accounts(request):
    user = request.user
    user_accounts = Account.objects.filter(user=user)
    return render(request, 'budgettrack/accounts.html', {
        'accounts': user_accounts
    })