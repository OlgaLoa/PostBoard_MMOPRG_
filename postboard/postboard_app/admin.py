from django.contrib import admin
from .models import User, Category, Post
from django_summernote.admin import SummernoteModelAdmin
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text_of_the_post',)

admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Category)

