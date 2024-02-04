from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True,
                               min_length=5)
    email = forms.EmailField(max_length=50, required=True)

    first_name = forms.CharField(max_length=30, required=True, validators=[
        RegexValidator(r'^[a-zA-Z]*$', message="First name should not contain numerics")])
    last_name = forms.CharField(max_length=30, required=True, validators=[
        RegexValidator(r'^[a-zA-Z]*$', message="Last name should not contain numerics")])

    gender = forms.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        widget=forms.RadioSelect(),
        required=True,
    )


class ProfileForm(forms.Form):
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), required=True, min_length=5)
    email = forms.EmailField(max_length=50, required=True)
    first_name = forms.CharField(max_length=30, required=True, validators=[
        RegexValidator(r'^[a-zA-Z]*$', message="First name should not contain numerics, only alphabets")])
    last_name = forms.CharField(max_length=30, required=True, validators=[
        RegexValidator(r'^[a-zA-Z]*$', message="Last name should not contain numerics, only alphabets")])
    gender = forms.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        widget=forms.RadioSelect(),
        required=True,
    )
    role = forms.CharField(max_length=10, required=False)