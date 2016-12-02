from django.shortcuts import render
from .models import Bank, Transaction
from .forms import RegistrationForm
from django.http import HttpResponseRedirect

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


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #

            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form':form })




#def registration(request):
#    errors = []
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        if not username:
#            errors.append('Enter the login')
#        elif len(username) < 5:
#            errors.append('login len less 5')
#
#        password = request.POST.get('password')
#        if not password:
#            errors.append('Enter the password')
#        elif len(password) < 6:
#            errors.apend('password len less 6')
#
#        password_repeat = request.POST.get('password2')
#
#        if password != password_repeat:
#            errors.append('passwords are not equal')
#        if not errors:
#            #
#
#            return HttpResponseRedirect('/login/')
#        return render(request, 'registration.html', {'errors':errors})

