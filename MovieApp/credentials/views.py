from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname, first_name=firstname, last_name=lastname, email=email,
                                                password=password)
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')

    return render(request, "register.html")


@login_required
def profile_view(request):
    # Get the current user
    user = request.user
    return render(request, 'profile_view.html', {'user': user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        # Get and update the user data
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        # Save the changes
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')

    return render(request, 'profile_edit.html', {'user': request.user})
