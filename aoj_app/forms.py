from django import forms

from .models import AuthUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ('email', 'first_name', 'last_name', 'address', 'city',
                  'state', 'country', 'zip_code', 'phone_number', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
