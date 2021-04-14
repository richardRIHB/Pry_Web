from django.forms import *
from django import forms
from django.forms import ModelForm
from Apps.User.models import User

class user_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['imagen'].widget.attrs['onchange'] = 'return validarInputFile()'

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'imagen', 'is_active'
        exclude = ['groups', 'user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_staff']
        widgets = {
            'first_name': TextInput(
                attrs={
                    'autofocus': "autofocus",
                    'placeholder': 'Ingrese sus nombres',
                    'required': 'True'
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'required': 'True'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                    'required': 'True'
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su password',
                    'required': 'True'
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                passw = self.cleaned_data['password']
                u = form.save(commit=False)
                user = User.objects.get(pk=u.pk)
                if user.password != passw:
                    u.set_password(passw)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups', 'imagen', 'password']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


