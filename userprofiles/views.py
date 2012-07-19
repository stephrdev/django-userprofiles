# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from userprofiles import settings as up_settings
from userprofiles.utils import get_form_class


def registration(request):
    RegistrationForm = get_form_class(up_settings.REGISTRATION_FORM)

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Automatically log this user in
            if up_settings.AUTO_LOGIN:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

            return redirect(up_settings.REGISTRATION_REDIRECT)

    else:
        form = RegistrationForm()

    return render(request, 'userprofiles/registration.html', {
        'form': form
    })

def registration_complete(request):
    return render(request, 'userprofiles/registration_complete.html', {
        'account_verification_active': up_settings.USE_ACCOUNT_VERIFICATION,
        'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS,
    })
