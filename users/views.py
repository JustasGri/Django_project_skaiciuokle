
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Jūsų paskyra sukurta! Galite pasijungti')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Jūsų paskyra atnaujinta!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        veiklos = request.user.veiklos.all()
        pajamos = 0
        islaidos = 0
        mokesciai = 0
        pelnas = 0
        
        for veikla in veiklos:
            pajama = veikla.suma_pajamos
            pajamos += pajama
            islaida = veikla.suma_islaidos_pasirinkimas
            islaidos += islaida
            mokestis = veikla.suma_mokesciai
            mokesciai += mokestis
            pelna = veikla.suma_pelnas
            pelnas +=pelna


    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pajamos': pajamos,
        'islaidos': islaidos,
        'mokesciai': mokesciai,
        'pelnas': pelnas,
    }

    return render(request, 'users/profile.html', context)
