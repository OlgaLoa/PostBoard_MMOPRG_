from django.urls import path
from .views import PostList, PostCreate, PostDetail, PostUpdate, ResponseCreate, AuthorResponseList, AuthorResponseDelete
from . import views

urlpatterns = [

   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),

   path('subscriptions/', views.subscriptions, name='subscriptions'),

   path('<int:pk>/response_create', ResponseCreate.as_view(), name='response_create'),
   path('response_list', AuthorResponseList.as_view(), name='response_list'),
   path('<int:pk>/response_delete', AuthorResponseDelete.as_view(), name='response_delete'),
   path('<int:pk>/response_accept', views.response_accept, name='response_accept'),
]