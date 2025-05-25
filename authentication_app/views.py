from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

    if request.method=='POST':  #when user submit form
        form = UserCreationForm(request.POST)   #it will take that form
        if form.is_valid():     #now check if form is valid then it will fetch the user detail
            user = form.save()
            login(request,user)     #once user detail is save, it will send request user to the login
            return redirect('login')
    else:
        initial_data = {'username':'', 'password1':'', 'password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request,'auth/register.html', {'form':form})

def login_view(request):
    if request.user.is_authenticated:   #Check if the current user is logged in or not
        logout(request)
        return redirect('login')

    if request.method=='POST':  #when user submit form
        form = AuthenticationForm(request, data = request.POST)   #it will take that data request
        if form.is_valid():     #check if form is valid then it will fetch the user detail
            user = form.get_user()
            login(request,user)     #once user detail get, it will send user to the login
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'form': form, 'error message': "Invalid username or password"})
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request,'auth/login.html', {'form':form})

@login_required(login_url='login')  # Redirects to login page if not authenticated
def dashboard_view(request):
    return render(request,'auth/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
