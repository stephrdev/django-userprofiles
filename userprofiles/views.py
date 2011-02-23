from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required

from userprofiles import settings as up_settings
from userprofiles.utils import get_registration_form

if up_settings.USERPROFILES_USE_PROFILE:
    @login_required
    def profile(request):
        return render_to_response('userprofiles/profile.html', {
            'user': request.user,
        }, context_instance=RequestContext(request))


if up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION:
    from userprofiles.models import AccountVerification

    def registration_activate(request, activation_key):
        activation_key = activation_key.lower()
        account = AccountVerification.objects.activate_user(activation_key)
        return render_to_response('userprofiles/registration_activate.html', {
            'account': account,
            'expiration_days': up_settings.USERPROFILES_ACCOUNT_VERIFICATION_DAYS
        }, context_instance=RequestContext(request))

def registration(request):
    RegistrationForm = get_registration_form(up_settings.USERPROFILES_REGISTRATION_FORM)

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            return redirect('userprofiles_registration_complete')
    else:
        form = RegistrationForm()

    return render_to_response('userprofiles/registration.html', {
        'form': form
    }, context_instance=RequestContext(request))

def registration_complete(request):
    return render_to_response('userprofiles/registration_complete.html', {
        'account_verification_active': up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION,
        'expiration_days': up_settings.USERPROFILES_ACCOUNT_VERIFICATION_DAYS,
    }, context_instance=RequestContext(request))

