from django.shortcuts import render
from .forms import RegistrationForm


# Create your views here.


#signin
def signin(request):
    return render(request,'accounts/login.html')

def register(request):
    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,'accounts/signup.html',context)


def signout(request):   
    pass