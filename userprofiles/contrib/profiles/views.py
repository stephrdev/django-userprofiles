# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, FormView

from userprofiles.mixins import LoginRequiredMixin
from userprofiles.settings import up_settings
from userprofiles.utils import get_form_class, get_profile_model


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles/profile.html'

    def get_context_data(self, **kwargs):
        return {
            'user': self.request.user,
        }

profile = ProfileView.as_view()


class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = get_form_class(up_settings.PROFILE_FORM)
    template_name = 'userprofiles/profile_change.html'

    def get_form_kwargs(self):
        kwargs = super(ProfileChangeView, self).get_form_kwargs()
        kwargs['instance'] = get_profile_model().objects.get(
            user=self.request.user)

        if up_settings.REGISTRATION_FULLNAME:
            kwargs['initial'].update({
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email
            })
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _(u'Profile changed'))
        return redirect(up_settings.PROFILE_CHANGE_DONE_URL)

profile_change = ProfileChangeView.as_view()
