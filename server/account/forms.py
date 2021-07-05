from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput,
                                help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(_('A user with that email already exists.'))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(_('A user with that username already exists.'))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The two password fields did not match.'))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_verified = True
        user.is_agree = True
        if commit:
            user.save()
        return user


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
