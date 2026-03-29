from django.contrib import admin
from .models import Post, Comment, Board

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Board)