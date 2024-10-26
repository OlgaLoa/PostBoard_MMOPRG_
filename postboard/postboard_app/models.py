from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.mail import send_mail
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

# МОДЕЛЬ АВТОРА-ПОЛЬЗОВАТЕЛЯ
class User(AbstractUser):
    code = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.username
# #Django не знает, какую страницу нужно открыть после создания поста.
# #мы можем убрать проблему, добавив метод get_absolute_url в модель.
#     def get_absolute_url(self):
#         return reverse('users/login')

# МОДЕЛЬ КАТЕГОРИИ
class Category(models.Model): #
    CATEGORY_CHOICES = (
        ('Танки', 'Tanks'),
        ('Хилы', 'Healers'),
        ('ДД', 'DD'),
        ('Торговцы', 'Traders'),
        ('Гилдмастеры', 'Guildmasters'),
        ('Квестгиверы', 'Questgivers'),
        ('Кузнецы', 'Blacksmiths'),
        ('Кожевники', 'Leatherworkers'),
        ('Зельевары', 'Potions_Masters'),
        ('Мастеразаклинаний', 'Spell_Masters'))
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='Tanks')  # поле с выбором категории;

    def __str__(self):
        return self.category

# МОДЕЛЬ ПОСТА
# Объявления состоят из заголовка и текста, внутри которого могут быть картинки, встроенные видео и другой контент.
# пользователь обязательно должен определить объявление в одну из категорий
class Post(models.Model):# содержать в себе статьи и новости, которые создают пользователи
    title_of_the_post = models.CharField(max_length=128)  # заголовок поста;
    text_of_the_post = models.TextField(null=True, blank=True ) # текст поста с изображ;
    category_of_the_post = models.ForeignKey(Category, on_delete = models.CASCADE)# у одной категории мб много постов;
    author_of_the_post = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания;

    def __str__(self):
        return self.title_of_the_post

#Django не знает, какую страницу нужно открыть после создания поста.
#мы можем убрать проблему, добавив метод get_absolute_url в модель.
    def get_absolute_url(self):
        return reverse('post_list') #ф-ия reverse, которая позволяет нам указывать название пути.


# МОДЕЛЬ ОТКЛИКА
# Пользователи могут отправлять отклики на объявления других пользователей, состоящие из простого текста.
class Response(models.Model):
    text_of_the_response = models.CharField(max_length=128)  # заголовок поста;
    post_of_the_response = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_of_the_response = models.ForeignKey(User, on_delete=models.CASCADE)
    response_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.post_of_the_response.title_of_the_post

# МОДЕЛЬ ПОДПИСКИ НА КАТЕГОРИЮ ПОСТА
class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions',)
