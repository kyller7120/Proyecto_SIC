from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required
def inicio(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('/')
