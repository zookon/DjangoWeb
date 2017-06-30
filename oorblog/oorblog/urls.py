"""oorblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import  include
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import DetailView
from kblog.models import BlogBody
from kblog.views import index, login, add_article, sub_article, person_info, article_list, login_check, sub_comment, \
    edit_article, sub_edit_article, article_edit_lists
from oorblog import settings
from kblog.views import article

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', index),
    url(r'^index/$', index,name = 'index'),
    url(r'^person_info/$', person_info,name = 'person_info'),
    url(r'^login/$', login,name='login'),
    url(r'^login_check/$', login_check,name='login_check'),
    url(r'^article/(?P<article_id>\d+)/$', #article_id 从views传递来的参数
        article, name='article'),
    url(r'^article_list/(?P<list_type>\d+)/$',
        article_list, name='article_list'),
    url(r'^add_article/', add_article, name='add_article'),
    url(r'^sub_article/', sub_article, name='sub_article'),
    url(r'^article_edit_lists/', article_edit_lists, name='article_edit_lists'),
    url(r'^edit_article/(?P<article_id>\d+)/$', edit_article, name='edit_article'),
    url(r'^sub_edit_article/(?P<article_id>\d+)/$', sub_edit_article, name='sub_edit_article'),# 函数需要用到的article_id从这里传入
    url(r'^sub_comment/', sub_comment, name='sub_comment'),
    url(r'', include('comments.urls',namespace='comments')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
