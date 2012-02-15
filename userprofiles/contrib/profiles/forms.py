# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from userprofiles import settings as up_settings
from userprofiles.utils import UserProfile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('E-mail'))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        if not up_settings.PROFILE_ALLOW_EMAIL_CHANGE:
            del self.fields['email']
        else:
            self.fields.keyOrder.remove('email')
            self.fields.keyOrder.insert(0, 'email')

        if not up_settings.REGISTRATION_FULLNAME:
            del self.fields['first_name']
            del self.fields['last_name']
        else:
            self.fields.keyOrder.remove('first_name')
            self.fields.keyOrder.remove('last_name')
            self.fields.keyOrder.insert(0, 'first_name')
            self.fields.keyOrder.insert(1, 'last_name')

    def save(self, *args, **kwargs):
        obj = super(ProfileForm, self).save(*args, **kwargs)
        if up_settings.REGISTRATION_FULLNAME:
            obj.user.first_name = self.cleaned_data['first_name']
            obj.user.last_name = self.cleaned_data['last_name']

        if up_settings.PROFILE_ALLOW_EMAIL_CHANGE:
            obj.user.email = self.cleaned_data['email']

        if up_settings.REGISTRATION_FULLNAME or up_settings.PROFILE_ALLOW_EMAIL_CHANGE:
            obj.user.save()

        if hasattr(self, 'save_profile'):
            self.save_profile(obj, *args, **kwargs)

        return obj

    class Meta:
        model = UserProfile
        exclude = ('user',)
