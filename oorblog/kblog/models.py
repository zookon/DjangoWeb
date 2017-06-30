# -*- coding:utf8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.
class User(models.Model):
    F_USER = models.CharField(max_length=50)
    F_PWD = models.CharField(max_length=50)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')

class UserInfo(models.Model):
    nickname = models.CharField(max_length=20)
    work = models.CharField(max_length=20)
    company = models.CharField(max_length=50)
    email = models.CharField(max_length=20)

class BlogBody(models.Model):
    blog_title = models.CharField(max_length=50)
    blog_body = models.TextField()
    blog_type = models.CharField(max_length=50)
    blog_timestamp = models.DateTimeField()
    blog_imgurl = models.CharField(max_length=50, null=True)
    blog_author = models.CharField(max_length=20)

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(BlogBody)

