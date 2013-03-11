# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from userprofiles.settings import up_settings
from userprofiles.utils import get_form_class


class RegistrationView(FormView):
    form_class = get_form_class(up_settings.REGISTRATION_FORM)
    template_name = 'userprofiles/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Automatically log this user in
        if up_settings.AUTO_LOGIN:
            if up_settings.EMAIL_ONLY:
                username = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)

        return redirect(up_settings.REGISTRATION_REDIRECT)

registration = RegistrationView.as_view()


class RegistrationCompleteView(TemplateView):
    template_name = 'userprofiles/registration_complete.html'

    def get_context_data(self, **kwargs):
        return {
            'account_verification_active': up_settings.USE_ACCOUNT_VERIFICATION,
            'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS,
        }

registration_complete = RegistrationCompleteView.as_view()
