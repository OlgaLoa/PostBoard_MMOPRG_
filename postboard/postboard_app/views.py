from .models import Post, User, Response, Subscription, Category
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import PostForm, ResponseForm
from django.urls import reverse_lazy
from .filters import PostOfResponseFilter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect



##############################################  ПОСТЫ   ################################################################
class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'id'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_list'

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['response'] = Response.objects.all()
        return context


#
class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = 'postboard_app.add_post' #add_post из админки Chosen permissions
    form_class = PostForm # Указываем нашу разработанную форму
    model = Post # модель
    template_name = 'post_create.html' #новый шаблон, в котором используется форма.


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):# Добавляем новое представление для обновления поста
    permission_required = 'postboard_app.change_post',
    form_class = PostForm # Указываем нашу разработанную форму
    model = Post # модель
    template_name = 'post_update.html' # и новый шаблон, в котором используется форма.
    # raise_exception = True

    #изменим метод PermissionRequiredMixin
    def dispatch(self, request, *args, **kwargs):
        name_of_author_updating = Post.objects.get(pk=self.kwargs.get('pk')).author_of_the_post.username #получаем имя автора
        if self.request.user.username == 'admin' or self.request.user.username ==  name_of_author_updating:#проверяем имя является ли админом или автором данного поста
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Извините, Вы не можете изменять данный пост, тк не являетесь его автором')

##############################################  ОТКЛИКИ   ################################################################
# СОЗДАНИЕ ОТКЛИКА
class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm # Указываем нашу разработанную форму
    model = Response # модель
    template_name = 'response_create.html' #новый шаблон, в котором используется форма.


    def form_valid(self, form):
        form.instance.post_of_the_response = Post.objects.get(pk=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')  # при успешной авторизации перенаправление на страницу всех постов


# ПРОСМОТР ОТКЛИКОВ АВТОРА ПОСТОВ
# пользователю должна быть доступна приватная страница с откликами на его объявления,
# checks whether the user accessing a view has all given permissions. You should specify the permission
# (or an iterable of permissions) using the permission_required parameter permission_required
class AuthorResponseList(LoginRequiredMixin, ListView):
    # permission_required = ('postboard_app.response',)
    model = Response # Указываем модель, объекты которой мы будем выводить
    template_name = 'response_list.html'
    context_object_name = 'response_list'  # Это имя списка, в котором будут лежать все объекты, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10
    ordering = 'id' # Поле, которое будет использоваться для сортировки объектов

    # Переопределяем функцию получения списка постов
    # находим отклики именно к АВТОРУ постов
    def get_queryset(self):
        queryset = Response.objects.filter(post_of_the_response__author_of_the_post=self.request.user)
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostOfResponseFilter(self.request.GET, queryset, request=self.request.user)  #request=self.request.user для фильтрации по постам АВТОРА
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


#УДАЛЕНИЕ ОТКЛИКА АВТОРОМ ПОСТА
class AuthorResponseDelete(LoginRequiredMixin, DeleteView):# Добавляем новое представление для удвления отклика автором.
    model = Response # модель
    template_name = 'response_delete.html' # и новый шаблон, в котором используется форма.
    success_url = reverse_lazy('response_list')# куда перенеправить поль-ля после удаления товара

#УДАЛЕНИЕ ОТКЛИКА АВТОРОМ ПОСТА
@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.response_accepted = True #ставим статус принятия отклика
        response.save()
        return HttpResponseRedirect('/posts/response_list')
    else:
        return HttpResponseRedirect('/users/login')

##############################################  ПОДПИСКИ   ##############################################################
#представление списка категорий, на которые подписан пользователь,
@login_required #могут использовать только зарегистрированные пользователи
@csrf_protect #будет автоматически проверяться CSRF-токен в получаемых формах
def subscriptions(request):#функция, кот считает подписки
    if request.method == 'POST': #когда пользователь нажмёт кнопку подписки или отписки от категории.
        category_id = request.POST.get('category_id')#присваиваем id категории на кот нажал пользователь
        category = Category.objects.get(id=category_id)#присваиваем значение категории на кот нажал пользователь
        action = request.POST.get('action') #присваиваем значение действия кот нажал пользователь

        if action == 'subscribe':#если нажал  'subscribe'::
            Subscription.objects.create(user=request.user, category=category)#создаем объект подписки по user и category
        elif action == 'unsubscribe':#если нажал отписаться:
            Subscription.objects.filter(user=request.user,category=category,).delete()#удаляем объект подписки с пом фильтра по user и category

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscription.objects.filter(
                user=request.user, category=OuterRef('pk'),))).order_by('category') #количество подписчиков к каждой категории отсорт по имени
    return render(request,'subscriptions.html',{'categories': categories_with_subscriptions},)
#Функция render() принимает объект запроса в качестве первого аргумента, имя шаблона в качестве второго аргумента и словарь в качестве необязательного третьего аргумента.
#Она возвращает объект HttpResponse данного шаблона, отображенный в данном контексте
# exists() Возвращает True, если QuerySet содержит какие-либо результаты, и False, если нет.
# Ссылка на столбцы из внешнего набора queryset class OuterRef(field)[исходныйкод]


