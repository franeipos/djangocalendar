from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    # last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Apellido')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # Override built-in style for the inputs
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

