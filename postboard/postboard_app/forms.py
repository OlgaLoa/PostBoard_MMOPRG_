from django import forms
from django_summernote.fields import SummernoteTextField, SummernoteTextFormField

from .models import Post, User, Response
from django_summernote.widgets import SummernoteWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

import string
import random

#
# # from .postboard import settings
# from django.core.mail import send_mail

# ФОРМА СОЗДАНИЯ ПОСТА
class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title_of_the_post',
            'author_of_the_post',
            'category_of_the_post',
            'text_of_the_post',
        ]
        widgets = {
            'text_of_the_post': SummernoteWidget(),
        }

# ФОРМА СОЗДАНИЯ ОТКЛИКА НА ЧУЖОЙ ПОСТ
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response

        fields = [
            'text_of_the_response',
            'author_of_the_response',
        ]