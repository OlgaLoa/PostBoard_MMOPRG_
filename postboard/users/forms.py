import random
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from postboard_app.models import User
from allauth.account.forms import SignupForm
from django.conf import  settings



#ФОРМА АВТОРИЗАЦИИ
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password'] # названия полей должны соответствовать стандартной модели пользователя User


#ФОРМА РЕГИСТРАЦИИ
class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username','email', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }
    #проверка уникальности email
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Такой E-mail уже существует!")
    #     return email

    # #сохраняем юзера с переданными данными и отправляем код на почту
    # def save_user_and_send_code(self, request):
    #     user = super(RegistrationUserForm, self).save(request)#сохраняем юзера с переданными данными в бд
    #     user.is_active = False #неактивный статус
    #     code = ''.join(random.sample(123456789, 4))  # формируем код
    #     user.code = code #присваиваем юзеру отправленный код
    #     user.save()#сохраняем юзера в бд
    #
    #     send_mail(
    #         subject=f'Код подтверждения email',
    #         message=f'Код подтверждения email: {code}',
    #         from_email='settings.DEFAULT_FROM_EMAIL',
    #         recipient_list=[user.email],
    #
    #     )
    #     return user



class Сonfirmation_with_code_form(forms.ModelForm):
    code = forms.CharField(label='Код из email', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['code']



