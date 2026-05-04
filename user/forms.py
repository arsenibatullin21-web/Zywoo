from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = UsernameField(max_length=100, required=True, label='Username')
    password = forms.CharField(required=True, label='Password')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = UsernameField(max_length=100, required=True, label='Username')
    password1 = forms.CharField(required=True, label='Password')
    password2 = forms.CharField(required=True, label='Repeat Password')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email' , 'phone','first_name', 'last_name', 'image','password1', 'password2']

        labels = {'username': 'Username',
                  'email': 'E-mail',
                  'password1': 'Password',
                  'password2': 'Repeat Password',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'phone': 'Phone Number',
                  'image': 'Profile Image'
                  }

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('Username is already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email is already exists")
        return email