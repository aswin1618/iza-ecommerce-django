from django.shortcuts import render


# Create your views here.


#signin
def signin(request):
    return render(request,'accounts/login.html')

def register(request):
    
    return render(request,'accounts/signup.html')


def signout(request):   
    pass