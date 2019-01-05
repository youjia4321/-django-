from django.shortcuts import render
from django.views.generic.base import View
from bloginfo.forms import AddForm, CommentForm
from bloginfo.models import BlogInfo, Comment, Category, Tag
from django.http import Http404
from pure_pagination import Paginator 
from django.db.models import Q
from datetime import datetime
from user.models import UserProfile
# Create your views here.


def check(className, name=None):
    try:
        cate = className.objects.get(name=name)
        if cate:
            return cate
    except Exception as e:
        return None

class AddView(View):
    def get(self, request):
        return render(request, 'addblog.html', {})

    def post(self, request):
        add_form = AddForm(request.POST)
        if add_form.is_valid():
            title = request.POST.get('title', '')
            if BlogInfo.objects.filter(title=title):
                return render(request, 'addblog.html', {'msg': "标题已存在,请换一个"})
            content = request.POST.get('content', '')
            author = request.POST.get('author', '')
            category = request.POST.get('category', '')
            tags = request.POST.get('tag', '')
            # print(tags)
            # print(type(tags))
            tag_list = tags.split(' ')
            cates = check(Category, name=category)
            if cates is not None:
                blog = BlogInfo.objects.create(title=title, author=author, content=content, category=cates)
                for t in tag_list:
                    tags = check(Tag, name=t)
                    if tags is not None:
                        t = Tag.objects.get(name=tags.name)
                        blog.tag.add(t)
                    else:
                        tag = Tag.objects.create(name=t)
                        blog.tag.add(tag)
            else:
                cates = Category.objects.create(name=category)
                blog = BlogInfo.objects.create(title=title, author=author, content=content, category=cates)
                for t in tag_list:
                    tags = check(Tag, name=t)
                    if tags is not None:
                        t = Tag.objects.get(name=tags.name)
                        blog.tag.add(t)
                    else:
                        tag = Tag.objects.create(name=t)
                        blog.tag.add(tag)

            blog_lists = BlogInfo.objects.all().order_by('-add_time')
            try:
                page = request.GET.get('page', 1)
            except:
                page = 1
            p = Paginator(blog_lists, 5, request=request)
            lists = p.page(page)
            return render(request, 'blog_list.html', {'blog_list':lists, 'page': p}) 
            # return render(request, 'addblog.html', {'msg': "添加成功,返回首页查看!"})
        else:
            return render(request, 'addblog.html', {'add_form': add_form})


class DeleteView(View):
    def get(self, request):
        blog_lists = BlogInfo.objects.filter(author=request.user.username).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 5, request=request)
        lists = p.page(page)
        return render(request, 'delete.html', {'blog_list': lists})

    def post(self, request):
        title = request.POST.get('title', '')
        blog = BlogInfo.objects.get(title=title)
        blog.delete()
        blog_lists = BlogInfo.objects.filter(author=request.user.username).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 5, request=request)
        lists = p.page(page)
        return render(request, 'delete.html', {'blog_list': lists})


class EditView(View):
    def get(self, request):
        blog_lists = BlogInfo.objects.filter(author=request.user.username).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 5, request=request)
        lists = p.page(page)
        return render(request, 'edit.html', {'blog_list': lists})

    def post(self, request):
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        return render(request, 'editadd.html', {'title': title, 'content': content})



def get_blogs(request):
    blog_lists = BlogInfo.objects.all().order_by('-add_time')
    try:
        page = request.GET.get('page', 1)
    except:
        page = 1
    p = Paginator(blog_lists, 5, request=request)
    lists = p.page(page)
    cate_list = Category.objects.all()[:8]
    return render(request, 'blog_list.html', {'blog_list':lists, 'page': p, 'cate_list': cate_list}) 


class EditAddView(View):
    def post(self, request):
        content = request.POST.get('content', '')
        title = request.POST.get('title', '')
        blog = BlogInfo.objects.get(title=title)
        blog.content = content
        blog.add_time = datetime.now()
        blog.save()
        return render(request, 'editadd.html', {'msg': "修改成功,返回查看!"})


def get_details(request,blog_id):
    blog = BlogInfo.objects.get(id=blog_id)  #获取固定的blog_id的对象；
    tags = blog.tag.all()
    if request.method == 'GET':
        if blog.author == request.user.username:
            blog.visit = blog.visit
        else:
            blog.visit = blog.visit + 1
        blog.save()
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            blog.visit = blog.visit + 1
            blog.save()
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')
            Comment.objects.create(blog=blog, name=username, email=email, content=content)
    
    ctx={
        'blog':blog,
        'comments': blog.comment_set.all().order_by('-pub'),
        'form': form,
        'tags': tags
    }
    return render(request,'blog_details.html',ctx)

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'results.html', {'error_msg': error_msg})
    title_list = BlogInfo.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__icontains=q) | Q(category__name__icontains=q)).order_by("-add_time")
    return render(request, 'results.html', {'error_msg': error_msg, 'title_list': title_list})



class EditInfo(View):
    def get(self, request):
        username = request.user.username
        user = UserProfile.objects.get(username=username)
        visits = BlogInfo.objects.filter(author=username)
        count = 0
        for visit in visits:
            count += visit.visit
        blog_lists = BlogInfo.objects.filter(author=username).order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 5, request=request)
        lists = p.page(page)
        return render(request, 'personal.html', {'blog_list': lists, 'page': p, 'user': user, 'count': count})

    def post(self, request):
        pass


class getPerson(View):
    def get(self, request):
        username = request.GET.get("user", "")
        user = UserProfile.objects.get(username=username)
        if user.username == request.user.username:  # 当自己访问自己的信息时访问量不增加
            user.visit = user.visit
        else:
            user.visit = user.visit + 1
        user.save()
        visits = BlogInfo.objects.filter(author=username)
        count = 0
        for visit in visits:
            count += visit.visit
        blog_lists = BlogInfo.objects.filter(author=username).order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 20, request=request)
        lists = p.page(page)
        return render(request, 'others.html', {'blog_list': lists, 'page': p, 'user': user, 'count': count})
