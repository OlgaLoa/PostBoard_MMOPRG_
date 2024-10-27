# Пользователи могут отправлять отклики на объявления других пользователей, состоящие из простого текста.
# При отправке отклика пользователь должен получить e-mail с оповещением о нём.
# Также пользователю должна быть доступна приватная страница с откликами на его объявления,
# внутри которой он может фильтровать отклики по объявлениям, удалять их и принимать
# (при принятии отклика пользователю, оставившему отклик, также должно прийти уведомление).
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *


# !!!НЕ ЗАБЫТЬ ЗАРЕГИСТРИРОВАТЬ СИГНАЛЫ в apps.py!!!

#СИГНАЛ СОЗДАТЕЛЮ ОТКЛИКА ОБ УСПЕШНОМ СОЗДАНИИ ОТКЛИКА
@receiver(post_save, sender = Response)#тип сигнала, модель
def signal_to_author_of_response(sender, instance, created, **kwargs):
    # sender- модель отправителя сигнала (Response),
    # instance - экземпляр модели , кот был сохранен (Response),
    # created - булевое: True - был создан нов экземпляр
    if created:  # проверяем был ли создан новый экземпляр Response
        #если был создан:
       user = instance.author_of_the_response #определяем, кто написал отклик
        #шлем ему письмо на почту
       send_mail(
           'Your response was created',
           f' Hello, {user.username}! You have successfully created a response.',
           from_email='settings.DEFAULT_FROM_EMAIL',
           recipient_list=[user.email],
           fail_silently=False
       )

# # СИГНАЛ АВТОРУ ПОСТА О СОЗАДНИИ ОТКЛИКА К ЕГО ПОСТУ
@receiver(post_save, sender=Response)  # тип сигнала, модель
def signal_to_author_of_post(sender, instance, created, **kwargs):
    if created:  # проверяем был ли создан новый экземпляр Response
            post = instance.post_of_the_response #определяем, к какому посту написан отклик
            user = post.author_of_the_post #определяем автора поста,к кот.написан отклик

            send_mail(
                    'To your post was created a response ',
                    f' Hello, {user.username}! To your post was created a response.',
                    from_email='settings.DEFAULT_FROM_EMAIL',
                    recipient_list=[user.email],
                    fail_silently=False
            )

# СИГНАЛ АВТОРУ ОТКЛИКА О ПРИНЯТИИ ОТКЛИКА АВТОРОМ ПОСТА
@receiver(post_save, sender=Response)  # тип сигнала, модель
def signal_to_author_of_response_about_accept(sender, instance, created = False, **kwargs): # created = False те был обновлен экземпляр ( а не создан новый)
    if not created:  # проверяем был ли создан новый экземпляр Response
        # если не был создан но был сохранен:
        user = instance.author_of_the_response  # определяем, кто написал отклик
        # шлем ему письмо на почту
        send_mail(
            'Your response was accepted',
            f' Hello, {user.username}! Your response was accepted by the author of the post.',
            from_email='settings.DEFAULT_FROM_EMAIL',
            recipient_list=[user.email],
            fail_silently=False
        )


#СИГНАЛ ПОДПИСЧИКУ О ПОЯВЛЕНИИ ПОСТА ПО ВЫБРАННОЙ КАТЕГОРИИ
@receiver(post_init, sender=Post)
def signal_to_the_subscriber_of_category(sender, instance, created = True, **kwargs): # created = True те был создан экземпляр
    if created:  # проверяем был ли создан новый экземпляр
        category_id = instance.category_of_the_post_id #получаем id категории созданного поста
        #Если вы получаете идентификатор категории, тогда и подписчиков получайте по идентификатору категории
        subscribers_of_the_category = User.objects.filter(subscriptions__category_id=category_id)

        emails = subscribers_of_the_category.values_list('email', flat=True) #flat=True to return a QuerySet of single values instead of 1-tuples:


        send_mail(
            'It was created a post by category you have interested ',
            f' Hello! It was created a post by category you have interested ',
            from_email='settings.DEFAULT_FROM_EMAIL',
            recipient_list=[emails],
            fail_silently=False
        )
