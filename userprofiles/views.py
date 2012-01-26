# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from userprofiles import settings as up_settings
from userprofiles.utils import get_form_class


def registration(request):
    RegistrationForm = get_form_class(up_settings.REGISTRATION_FORM)

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            return redirect('userprofiles_registration_complete')
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
