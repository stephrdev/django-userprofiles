from django import forms
from .models import Profile

from userprofiles.forms import RegistrationForm


class ProfileRegistrationForm(RegistrationForm):
    short_info = forms.CharField(widget=forms.Textarea)

    def save_profile(self, new_user, *args, **kwargs):
        Profile.objects.create(
            user=new_user,
            short_info=self.cleaned_data['short_info']
        )
