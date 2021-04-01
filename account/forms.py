from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, required=True,
                               widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=6, required=True,
                                            widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmation',
                  'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким юзернеймом уже существует')
        return username


    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.pop('password_confirmation')
        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        else:
            return data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        return user







