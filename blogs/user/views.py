from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
from user.models import UserProfile, EmailCodeRecord, MessageModel
from django.contrib.auth import login, logout
from user.forms import LoginForm, RegisterForm, ModifyPwdForm, ForgetPwdForm, ChangeInfoForm, MessageForm, ImageUploadForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_email_register
from bloginfo.models import BlogInfo, Category, Comment
from bloginfo.views import get_blogs
from pure_pagination import Paginator



def check(username=None, password=None):
    try:
        user = UserProfile.objects.get(Q(username=username) | Q(email=username))
        if user.check_password(password):
            return user
    except Exception as e:
        return None
        

class Login(View):
    def get(self, request):
        blog_lists = BlogInfo.objects.all().order_by('-add_time')[:2]
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 3, request=request)
        lists = p.page(page)
        return render(request, 'home.html', {'blog_list': lists})


class LoginView(View):
    def get(self, request):
        return render(request, 'login_user.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = check(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    blog_lists = BlogInfo.objects.all().order_by('-add_time')
                    try:
                        page = request.GET.get('page', 1)
                    except:
                        page = 1
                    p = Paginator(blog_lists, 5, request=request)
                    lists = p.page(page)
                    cate_list = Category.objects.all()[:8]
                    return render(request, 'blog_list.html', {'blog_list':lists, 'page': p, 'cate_list': cate_list}) 
                else:
                    return render(request, 'login_user.html', {'msg': "用户没有激活"}) 
            else:
                return render(request, 'login_user.html', {'msg': "用户不存在或密码错误"}) 
        else:
            user_name = request.POST.get('username', '')
            return render(request, 'login_user.html', {'username': user_name,'login_form': login_form})


def logoutView(request):
    logout(request)
    blog_lists = BlogInfo.objects.all().order_by('-add_time')[:2]
    try:
        page = request.GET.get('page', 1)
    except:
        page = 1
    p = Paginator(blog_lists, 3, request=request)
    lists = p.page(page)
    return render(request, 'home.html', {'blog_list': lists})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get("password", '')
            user_name = request.POST.get("username", '')
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'register.html', {'msg': '此用户名已被使用'})
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_email_register(email, 'register')
            return render(request, 'login_user.html', {'msg': "发送邮件成功，请注意查收..."})
        else:
            email = request.POST.get("email", '')
            return render(request, 'register.html', {'email': email, 'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        records = EmailCodeRecord.objects.filter(code=active_code)
        if records:
            for record in records: 
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login_user.html',{'msg': '用户已激活'})


class ResetView(View):
    def get(self, request, active_code):
        records = EmailCodeRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, "login_user.html", {})


class ModifyView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login_user.html', {'msg': '修改密码成功'})
        else:
            email = request.POST.get("email", '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            user = UserProfile.objects.filter(email=email)
            if user:
                send_email_register(email, 'forget')
                return render(request, 'login_user.html', {'msg': "邮件发送成功，请查收..."})
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '邮箱错误'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class Modify(View):
    def get(self, request):
        modify_form = ModifyPwdForm()
        return render(request, 'modify.html', {})

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            user = check(username=email, password=password)
            if user is not None:
                if pwd1 != pwd2:
                    return render(request, 'modify.html', {'msg': '两次密码不一致'})
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login_user.html', {'msg': '修改密码成功,请登录'})
            else:
                return render(request, 'modify.html', {'msg': '邮箱号不存在或密码错误'})
        else:
            return render(request, 'modify.html', {'modify_form': modify_form})



def contact(request):
    return render(request, 'contact.html', {})



class ChangeInfo(View):
    def get(self, request):
        username = request.user.username
        user = UserProfile.objects.get(username=username)
        blog_lists = BlogInfo.objects.filter(author=username).order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 20, request=request)
        lists = p.page(page)
        return render(request, 'changeinfo.html', {'blog_list': lists, 'page': p, 'user': user})

    def post(self, request):
        change_form = ChangeInfoForm(request.POST)
        if change_form.is_valid():
            name = request.POST.get('name', '')
            username = request.POST.get('username', '')
            mood = request.POST.get('mood', '')
            nick = request.POST.get('nick', '')
            gender = request.POST.get('gender', '')
            birthday = request.POST.get('birthday', '')
            address = request.POST.get('address', '')
            user = UserProfile.objects.get(username=name)
            user.username = username
            user.nick_name= nick
            user.mood = mood
            user.gender = gender
            user.birthday = birthday
            user.address = address
            user.save()
            comments = Comment.objects.filter(name=name)
            for comment in comments:
                comment.name = username
                comment.save()
            blogs = BlogInfo.objects.filter(author=name)
            for blog in blogs:
                blog.author = username
                blog.save()
            blog_lists = BlogInfo.objects.filter(author=username).order_by("-add_time")
            try:
                page = request.GET.get('page', 1)
            except:
                page = 1
            p = Paginator(blog_lists, 20, request=request)
            lists = p.page(page)
            return render(request, 'personal.html', {'blog_list': lists, 'page': p, 'user': user})
        else:
            username = request.user.username
            user = UserProfile.objects.get(username=username)
            blog_lists = BlogInfo.objects.filter(author=username).order_by("-add_time")
            try:
                page = request.GET.get('page', 1)
            except:
                page = 1
            p = Paginator(blog_lists, 20, request=request)
            lists = p.page(page)
            return render(request, 'changeinfo.html', {'blog_list': lists, 'page': p, 'user': user, 'change_form': change_form})


class Message(View):
    def get(self, request):
        user = request.user.username
        message_lists = MessageModel.objects.all().order_by("-pub")
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(message_lists, 7, request=request)
        lists = p.page(page)
        return render(request, 'visitmessage.html', {'message_lists': lists, 'page': p})

    def post(self, request):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = request.POST.get('message', '')
            username = request.POST.get('username', '') 
            user = UserProfile.objects.get(username=username)
            MessageModel.objects.create(user=user, name=username, content=message)
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
            return render(request, 'others.html', {'blog_list': lists, 'page': p, 'user': user, 'count': count, 'msg': '留言成功'})
        else:
            return render(request, 'others.html', {'message_form': message_form})            


def changeimage(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        request.user.image = image
        request.user.save()
        visits = BlogInfo.objects.filter(author=request.user.username)
        count = 0
        for visit in visits:
            count += visit.visit
        blog_lists = BlogInfo.objects.filter(author=request.user.username).order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(blog_lists, 20, request=request)
        lists = p.page(page)
        return render(request, 'personal.html', {'blog_list': lists, 'page': p, 'user': request.user, 'count': count})
    else:
        user = request.user
        return render(request, 'imageset.html', {'user': user})
    