from django.urls import path
from .views import LoginUser
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [

   path('login/', LoginUser.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('registration/', views.registration, name='registration'),
   path('code/',  views.check_code_and_save_user, name='code'),


]