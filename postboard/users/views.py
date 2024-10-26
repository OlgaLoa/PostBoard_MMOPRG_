from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegistrationUserForm, Сonfirmation_with_code_form
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django import forms
from postboard_app.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
from django.http import HttpResponseRedirect, HttpResponse


# КЛАСС АВТОРИЗАЦИИ ПОЛЬЗОВАТЕЛЯ
class LoginUser(LoginView):
    form_class = LoginUserForm  # стандартный класс формы фреймворка Django с набором определенных методов и атрибутов, кот. работает в связке с LoginView
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('post_list')  # при успешной авторизации перенаправление на страницу всех постов


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ И ОТПРАВКА КОДА НА ПОЧТУ
def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST) #создаем форму с переданными в нее данными через POST
        if form.is_valid():#если корректно заполнена форма, то
            user = form.save(commit=False)#создаем юзера без занесения в бд
            code = ''.join(random.sample('123456789', 4))  # формируем код
            user.code = code  # присваиваем юзеру отправленный код
            user.is_active = False# присваиваем юзеру неактивный статус
            user.save() #заносим созданного (с кодом и неакт. статусом) юзера в бд

            # высылаем письмо юзеру
            send_mail(
                    subject=f'Код подтверждения email',
                    message=f'Код подтверждения email: {code}',
                    from_email='settings.DEFAULT_FROM_EMAIL',
                    recipient_list=[user.email],)

        return redirect('code')
    else:
        form = RegistrationUserForm()#если GET, то формируем пустую форму
        return render(request, 'users/code.html', {'form': form})


# ПРОВЕРКА ВВЕДЕННОГО ПОЛЬЗОВАТЕЛЕМ КОДА И ЗАВЕРШЕНИЕ РЕГИСТРАЦИИ
def check_code_and_save_user(request):
    if request.method == 'POST':
        form = Сonfirmation_with_code_form(request.POST)  #создаем форму с переданными в нее данными через POST
        if form.is_valid():  # если корректно заполнена форма, то
            if 'code' in request.POST:
                user = User.objects.filter(code=request.POST['code'])
                if user.exists():
                    user.update(is_active=True)
                # User.objects.filter(code=request.POST['code']).update(is_active=True)
                    return redirect('login')
                else:
                    return render(request,"users/invalid_code.html",)
    else:
        form = Сonfirmation_with_code_form()
        return render(request, 'users/code.html', {'form': form})


# def check_code_and_save_user(request):
#     if request.method == 'POST':
#         form = Сonfirmation_with_code_form(request.POST)  #создаем форму с переданными в нее данными через POST
#         if form.is_valid():  # если корректно заполнена форма, то
#             if 'code' in request.POST:
#                 user = User.objects.filter(code=request.POST['code'])
#                 if user.exists():
#                     user.update(is_active=True)
#                 # User.objects.filter(code=request.POST['code']).update(is_active=True)
#                     return redirect('login')
#
#     else:
#         form = Сonfirmation_with_code_form()
#         return render(request, 'users/code.html', {'form': form})





