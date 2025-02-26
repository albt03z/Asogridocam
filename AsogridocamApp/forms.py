from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    """ Formulario de registro de usuarios """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        """ Valida que el nombre de usuario sea único y cumpla con los requisitos """
        username = self.cleaned_data.get('username')
        
        if len(username) < 4:
            raise ValidationError("El nombre de usuario debe tener al menos 4 caracteres")
        
        if not re.match("^[a-zA-Z0-9_]*$", username):
            raise ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso")
            
        return username

    def clean_email(self):
        """ Valida que el correo electrónico sea único y no pertenezca a dominios de prueba """
        email = self.cleaned_data.get('email')
        
        if email and email.split('@')[1].lower() in ['example.com', 'test.com']:
            raise ValidationError("Por favor usa una dirección de correo válida")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado")
            
        return email

    def clean_password1(self):
        """ Valida que la contraseña cumpla con los requisitos """
        password = self.cleaned_data.get('password1')
        
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe contener al menos un número")
        
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe contener al menos una mayúscula")
        
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial")
            
        return password

    def clean_first_name(self):
        """ Valida que el nombre cumpla con los requisitos """
        first_name = self.cleaned_data.get('first_name')
        
        if len(first_name) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        
        if not first_name.replace(" ", "").isalpha():
            raise ValidationError("El nombre solo puede contener letras")
            
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        if len(last_name) < 2:
            raise ValidationError("El apellido debe tener al menos 2 caracteres")
        
        if not last_name.replace(" ", "").isalpha():
            raise ValidationError("El apellido solo puede contener letras")
  
        return last_name.title()

    def clean(self):
        """ Valida que la contraseña no contenga el nombre de usuario y que las contraseñas coincidan """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if password1 and username and username.lower() in password1.lower():
            raise ValidationError("La contraseña no puede contener tu nombre de usuario")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        """ Guarda el usuario en la base de datos """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"].title() 
        user.last_name = self.cleaned_data["last_name"].title() 
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """ Formulario de inicio de sesión """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        """ Valida que el nombre de usuario sea válido """
        username = self.cleaned_data.get('username')
        
        if not User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario no existe")
            
        return username
    
    def clean(self):
        """ Valida que la contraseña sea correcta """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password and not User.objects.filter(username=username, password=password).exists():
            raise ValidationError("La contraseña es incorrecta")
            
        return cleaned_data