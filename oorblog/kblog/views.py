
# -*- coding: utf-8 -*-
import markdown
import pygments
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, render

from comments.forms import CommentForm
from comments.models import Comment
from kblog.models import User, UserInfo, BlogBody


def index(request):
    userinfo = UserInfo.objects.first() # 个人信息
    blog_body = BlogBody.objects.order_by('-blog_timestamp').all() # 文章内容
    paginator = Paginator(blog_body,6) # 实例化文章列表，同时2个一页
    page = request.GET.get('page')
    try:
        art_pagelist=paginator.page(page)
    except PageNotAnInteger:
        art_pagelist=paginator.page(1)
    except EmptyPage:
        art_pagelist = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/index.html',
                  {'userinfo': userinfo, 'article_lists':art_pagelist})

def login(req):
    print(req.POST)
    global username
    global password
    if 'username' in req.POST:
        username = req.POST['username']
        password = req.POST['password']
        print(username,password)
    else:
        username = "Not inputUserName"
    # ctx={
    #     'user':username,
    #     'pass':password,
    # }
    # 获取的表单数据与数据库进行比较
    #user = User.objects.filter(F_USER__exact=username, F_PWD__exact=password)
    user = authenticate(username=username, password=password)
    print(user)
    print(User.objects.filter)
    if user:
        return article_edit_lists(req)
        # # 比较成功，跳转文章列表编辑
        # response = render_to_response('blog/add_article.html')
        # # 将username写入浏览器cookie,失效时间为3600
        # response.set_cookie('username', username, 3600)
        # return response
    else:
        # 比较失败，还在login
        return render_to_response('login/login.html')
    # return render_to_response('login/login.html')

# 文章内容页面
def article(request, article_id):
    blog_content = BlogBody.objects.get(id=article_id) #正文
    blog_body = BlogBody.objects.all()[:6] # 侧边目录
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = blog_content.comment_set.all()
    # 将文章内容转换成markdown格式
    # blog_content.blog_body = markdown.markdown(blog_content.blog_body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'blog_content': blog_content,
               'form': form,
               'comment_list': comment_list,
               'blog_body': blog_body
               }
    return render(request, 'blog/Article.html', context=context)

# 文章列表页面
def article_list(request, list_type):
    #sql = 'select id, blog_title, blog_type, blog_timestamp, blog_body from kblog_blogbody WHERE blog_type LIKE "'+list_type+'%%" order by blog_timestamp desc'
    #article_lists = BlogBody.objects.raw(sql)
    article_lists = BlogBody.objects.order_by('-blog_timestamp').filter(blog_type__startswith=list_type).all()
    paginator = Paginator(article_lists, 12)  # 实例化文章列表，同时2个一页
    page = request.GET.get('page')
    try:
        art_lists = paginator.page(page)
    except PageNotAnInteger:
        art_lists = paginator.page(1)
    except EmptyPage:
        art_lists = paginator.page(paginator.num_pages)
    return render(request, 'blog/article_lists.html', {'article_lists': art_lists})

# 写文章页面跳转
def add_article(request):
    return render(request, 'blog/add_article.html')

# 文章内容提交处理
def sub_article(request):
    try:
        if request.method == 'POST':
            mytype = request.POST['article_type']
            title = request.POST['article_title']
            body = request.POST['article_editor']
            updb = BlogBody(blog_title=title, blog_body=body, blog_type=mytype, blog_author='张宏奎')
            updb.save()
            return index(request)
        else:
            print(request.method)
            return messages.Error(request.method)
    except Exception as e:
        print("错误：", e)

# 文章内容修改页面
def edit_article(request,article_id):
    blog_content = BlogBody.objects.get(id=article_id)  # 正文
    # 将文章作为模板变量传给 edit_article.html 模板，以便渲染相应数据。
    context = {
        'blog_content': blog_content,
    }
    return render(request, 'blog/edit_article.html', context=context)

# 文章列表编辑及新增
def article_edit_lists(request):
    article_lists = BlogBody.objects.order_by('-blog_timestamp').all()
    paginator = Paginator(article_lists, 12)  # 实例化文章列表，同时2个一页
    page = request.GET.get('page')
    try:
        art_lists = paginator.page(page)
    except PageNotAnInteger:
        art_lists = paginator.page(1)
    except EmptyPage:
        art_lists = paginator.page(paginator.num_pages)
    return render(request, 'blog/article_edit_lists.html', {'article_lists': art_lists})

# 文章内容修改提交处理
def sub_edit_article(request,article_id):
    try:
        if request.method == 'POST':
            mytype = request.POST['article_type']
            title = request.POST['article_title']
            body = request.POST['article_editor']
            BlogBody.objects.filter(id=article_id).update(blog_title=title, blog_body=body, blog_type=mytype)
            return index(request)
        else:
            print(request.method)
            return messages.Error(request.method)
    except Exception as e:
        print("错误：", e)

# 留言提交处理
def sub_comment(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            text = request.POST['message']
            post_id=request.POST['post_id']
            updb = Comment(name=name, email=email, text=text, post_id=post_id)
            updb.save()
            return article(request, post_id)
        else:
            print(request.method)
            return messages.Error(request.method)
    except Exception as e:
        print("错误：", e)

# 个人信息
def person_info(request):
    return render(request,'homepage/index.html')

# 写文章的登录验证界面
def login_check(request):
    return render(request,'login/login.html')