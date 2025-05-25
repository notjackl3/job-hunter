from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

class CustomPasswordResetForm(forms.Form):
    identifier = forms.CharField(label=_("Email/Username"), max_length=254)

    def get_users(self, identifier):
        if '@' in identifier:
            return User.objects.filter(email__iexact=identifier, is_active=True)
        else:
            return User.objects.filter(username__iexact=identifier, is_active=True)
    
    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        users = self.get_users(identifier)

        if not users.exists():
            raise ValidationError("No user found with that email or username.")

        if users.count() > 1:
            usernames = ", ".join(user.username for user in users)
            raise ValidationError(f"Multiple users found: {usernames}. Please enter a Username instead.")

        return identifier

    def save(self, **kwargs):
        identifier = self.cleaned_data["identifier"]
        user = self.get_users(identifier).first()

        reset_form = PasswordResetForm({'email': user.email})
        if reset_form.is_valid():
            reset_form.save(**kwargs)


