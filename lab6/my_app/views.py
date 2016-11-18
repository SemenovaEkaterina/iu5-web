from django.shortcuts import render
from .models import User, Bank, Transaction
from django.http import HttpResponse

def index(request):
    #posts = []
    #for i in range(10):
    #    posts.append({ 'header':'header ' + str(i), 'text': ( ' text ' + str(i) ) * 20, 'id': i })
    banks = Bank.objects.all()
    return render(request, "index.html", {'banks': banks})

def post(request, id):
    bank = Bank.objects.get(id=id)
    transactions = Transaction.objects.select_related('user').filter(bank=bank)
    return render(request, "post.html", {'bank': bank, 'transactions': transactions})
    #return HttpResponse("Here's the text of the Web page.")