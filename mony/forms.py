from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="First name", widget = forms.TextInput(attrs = {'class': 'form-control'}))
    last_name = forms.CharField(label="Last name", widget = forms.TextInput(attrs = {'class': 'form-control'}))
    email = forms.CharField(label="Email", max_length=128, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmation = forms.CharField(label="Confirm password", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=128, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
