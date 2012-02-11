# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from userprofiles import settings as up_settings
from userprofiles.contrib.emailverification.forms import ChangeEmailForm
from userprofiles.contrib.emailverification.models import EmailVerification


@login_required
def email_change(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            verification = form.save(request.user)
            return redirect('userprofiles_email_change_requested')
    else:
        form = ChangeEmailForm()

    return render(request, 'userprofiles/email_change.html', {'form': form})


@login_required
def email_change_requested(request):
    return render(request, 'userprofiles/email_change_requested.html', {
        'expiration_days': up_settings.EMAIL_VERIFICATION_DAYS})


@login_required
def email_change_approve(request, token, code):
    try:
        verification = EmailVerification.objects.get(token=token, code=code,
            user=request.user, is_expired=False, is_approved=False)

        verification.is_approved = True
        verification.save()
        messages.success(request, _(u'E-mail address changed to %(email)s' % {
            'email': verification.new_email}))
    except EmailVerification.DoesNotExist:
        messages.error(request,
            _(u'Unable to change e-mail address. Confirmation link is invalid.'))

    return redirect(up_settings.EMAIL_VERIFICATION_DONE_URL)
