# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _

from userprofiles import settings as up_settings
from userprofiles.utils import get_form_class


@login_required
def profile(request):
    return render_to_response('userprofiles/profile.html', {
        'user': request.user,
    }, context_instance=RequestContext(request))


@login_required
def profile_change(request):
    ProfileForm = get_form_class(up_settings.PROFILE_FORM)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
            instance=request.user.get_profile())
        if form.is_valid():
            profile = form.save()
            messages.success(request, _(u'Profile changed'))
            return redirect(up_settings.PROFILE_CHANGE_DONE_URL)
    else:
        if up_settings.REGISTRATION_FULLNAME:
            form = ProfileForm(instance=request.user.get_profile(), initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            })
        else:
            form = ProfileForm(instance=request.user.get_profile())

    return render(request, 'userprofiles/profile_change.html', {'form': form})
