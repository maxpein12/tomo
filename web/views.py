from django.shortcuts import redirect, render

def home(request):
    return redirect('dashboard:landing')

def PrivacyAndPolicy(request):
    return render(request, 'privacyandpolicy.html')

def UserDeletionRequest(request):
    return render(request, 'userdelete.html')

