from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UserProfileForm
from .models import UserProfile


def signup(request):
    """Inscription utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(user=user)
            messages.success(request, 'Inscription réussie ! Veuillez vous connecter.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Connexion utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Identifiant ou mot de passe incorrect.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Déconnexion utilisateur"""
    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    """Affiche et édite le profil utilisateur"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile_obj = form.save()
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form})
