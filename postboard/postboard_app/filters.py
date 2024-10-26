# Также пользователю должна быть доступна приватная страница с откликами на его объявления,
# внутри которой он может фильтровать отклики по объявлениям
from django_filters import FilterSet, ModelChoiceFilter
from .models import Post


class PostOfResponseFilter(FilterSet):
     post_of_the_response= ModelChoiceFilter( #создали фильтр с названием post_of_the_response
            field_name='post_of_the_response',#фильтрация будет проиходить по полю post
            queryset=Post.objects.all(),   #содержит значения в списке, кот б ВСЕ доступны
            label='post_of_the_response',   #название поля фильтра
            empty_label='all_posts')#фильтрация по всем, те без фильтрации (для верхней строки поиска)

     def get_queryset(self):
         queryset = super().get_queryset().all()

         if self.request.user.is_authenticated:
            queryset = queryset.filter(post__author_of_the_post=self.request.user)
         # Сохраняем нашу фильтрацию в объекте класса,
         # чтобы потом добавить в контекст и использовать в шаблоне.
            return queryset





    # # Переопределяем функцию получения списка товаров
    #  def get_queryset(self):
    #      queryset = Post.objects.filter(post__author_of_the_post=self.request.user)
    #      # Сохраняем нашу фильтрацию в объекте класса,
    #      # чтобы потом добавить в контекст и использовать в шаблоне.
    #      self.filterset = Post(self.request.GET, queryset)
    #      # Возвращаем из функции отфильтрованный список товаров
    #      return self.filterset.qs
    #      return queryset
# class PostOfResponseFilter(FilterSet):
#      post_of_the_response= ModelChoiceFilter( #создали фильтр с названием post_of_the_response
#             field_name='post_of_the_response',#фильтрация будет проиходить по полю post
#             queryset=Response.objects.all(),   #содержит значения в списке, кот б ВСЕ доступны
#             label='post_of_the_response',   #название поля фильтра
#             empty_label='all_posts')#фильтрация по всем, те без фильтрации

