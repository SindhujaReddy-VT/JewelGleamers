from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Details
from .forms import RegistrationForm, ProfileForm
from actions.models import Action


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create(username=username, email=email, password=password, first_name=first_name,
                                       last_name=last_name)
            details, created = Details.objects.get_or_create(user=user)
            gender = form.cleaned_data['gender']
            details.gender = gender
            details.save()
            request.session['username'] = user.username
            request.session['role'] = details.role
            messages.success(request, f"You have successfully registered with username: {user.username}")
            return redirect('jewelGleamer:logged_user_home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, "users/user/register.html", {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.session.get('role') == 'Admin' or user.username == request.session.get('username'):
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                user.password = form.cleaned_data['password']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                gender = form.cleaned_data['gender']
                user.save()
                details, created = Details.objects.get_or_create(user=user)
                details.gender = gender
                if user.username != request.session.get('username'):
                    role = form.cleaned_data['role']
                    old_role = details.role
                    details.role = role
                details.save()
                if user.username != request.session.get('username'):
                    if old_role != form.cleaned_data['role']:
                        action = Action(
                            user=user,
                            verb="role changed from "+old_role+" to "+form.cleaned_data['role'],
                            role_changed=True,
                        )
                        action.save()
                messages.success(request, "You have updated the details successfully")
        else:
            form = ProfileForm(initial={
                'password': user.password,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.details.gender if hasattr(user, 'details') else None,
                'role': user.details.role if hasattr(user, 'details') else None
            })
    else:
        actions = Action.objects.filter(user_id=user.id).order_by('-created')
        return render(request, 'users/user/profile.html', {"user": user, "actions": actions})
    actions = Action.objects.filter(user_id=user.id).order_by('-created')
    return render(request, 'users/user/profile.html', {"user": user, 'form': form,
                                                       "actions": actions})


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user is not None and (password == user.password):
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS, "You have logged in successfully")
        return redirect('jewelGleamer:logged_user_home')
    else:
        messages.add_message(request, messages.ERROR, "Invalid Username or Password")
    return render(request, 'users/user/login.html')


# Logout View
def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('jewelGleamer:home')


def login_page(request):
    return render(request,"users/user/login.html")


def user_profiles(request):
    user_names = User.objects.values_list('username', flat=True)
    return render(request, 'users/user/user_profiles.html', {'user_names': user_names})
