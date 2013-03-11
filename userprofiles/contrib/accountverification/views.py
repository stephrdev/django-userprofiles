# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from userprofiles.contrib.accountverification.models import AccountVerification
from userprofiles.settings import up_settings


class RegistrationActivateView(TemplateView):
    template_name = 'userprofiles/registration_activate.html'

    def get_context_data(self, **kwargs):
        activation_key = kwargs['activation_key'].lower()
        account = AccountVerification.objects.activate_user(activation_key)

        return {
            'account': account,
            'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS
        }

registration_activate = RegistrationActivateView.as_view()
