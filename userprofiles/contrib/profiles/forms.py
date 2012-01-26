# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from userprofiles import settings as up_settings
from userprofiles.utils import UserProfile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(_('First name'), required=False)
    last_name = forms.CharField(_('Last name'), required=False)
    email = forms.EmailField(_('E-mail'))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if not up_settings.REGISTRATION_FULLNAME:
            del self.fields['first_name']
            del self.fields['last_name']

        if not up_settings.PROFILE_ALLOW_EMAIL_CHANGE:
            del self.fields['email']

    def save(self, *args, **kwargs):
        obj = super(ProfileForm, self).save(*args, **kwargs)
        if up_settings.REGISTRATION_FULLNAME:
            obj.user.first_name = self.cleaned_data['first_name']
            obj.user.last_name = self.cleaned_data['last_name']
            obj.user.email = self.cleaned_data['email']
            obj.user.save()

        if hasattr(self, 'save_profile'):
            self.save_profile(obj, *args, **kwargs)

        return obj

    class Meta(object):
        model = UserProfile
        exclude = ('user',)
