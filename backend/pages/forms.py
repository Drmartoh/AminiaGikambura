from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'member'
        user.is_approved = False
        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
