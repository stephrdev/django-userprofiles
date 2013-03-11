# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView, RedirectView

from userprofiles.contrib.emailverification.forms import ChangeEmailForm
from userprofiles.contrib.emailverification.models import EmailVerification
from userprofiles.mixins import LoginRequiredMixin
from userprofiles.settings import up_settings


class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'userprofiles/email_change.html'
    form_class = ChangeEmailForm

    def form_valid(self, form):
        form.save(self.request.user)
        return redirect('userprofiles_email_change_requested')

email_change = EmailChangeView.as_view()


class EmailChangeRequestedView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles/email_change_requested.html'

    def get_context_data(self, **kwargs):
        return {
            'expiration_days': up_settings.EMAIL_VERIFICATION_DAYS
        }

email_change_requested = EmailChangeRequestedView.as_view()


class EmailChangeApproveView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, token, code):
        try:
            verification = EmailVerification.objects.get(token=token, code=code,
                user=self.request.user, is_expired=False, is_approved=False)

            verification.is_approved = True
            verification.save()

            messages.success(self.request, _(u'E-mail address changed to %(email)s' % {
                'email': verification.new_email}))

        except EmailVerification.DoesNotExist:
            messages.error(self.request,
                _(u'Unable to change e-mail address. Confirmation link is invalid.'))

        return reverse(up_settings.EMAIL_VERIFICATION_DONE_URL)

email_change_approve = EmailChangeApproveView.as_view()
