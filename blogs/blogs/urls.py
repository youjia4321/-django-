"""blogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from user import views
from django.conf.urls import url
from .settings import MEDIA_ROOT
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from user.views import LoginView, RegisterView, ActiveView, Login, ModifyView, ForgetPwdView, ResetView, Modify, contact, ChangeInfo, Message, changeimage
from bloginfo.views import AddView, DeleteView, EditView, EditAddView, get_blogs, get_details, search, EditInfo, getPerson

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="home.html"), name='login'),
    path('', Login.as_view(), name='home'),
    url('captcha/', include("captcha.urls")),
    url(r'^tinymce/', include('tinymce.urls')),
    path('register', RegisterView.as_view(), name="register"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_wpd'),
    url(r'^modify_pwd/$', ModifyView.as_view(), name='modify_pwd'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url('login', LoginView.as_view(), name='user_login'),
    path('logout', views.logoutView, name='logout'),
    path('forgetpwd', ForgetPwdView.as_view(), name='forgetpwd'),
    path('addBlog', AddView.as_view(), name='addblog'),
    path('blogList', get_blogs, name='index'),
    path('modify', Modify.as_view(), name='modify'),
    path('contact', contact, name='contact'),
    path('deleteBlog', DeleteView.as_view(), name='delete'),
    path('editBlog', EditView.as_view(), name='edit'),
    path('editAdd', EditAddView.as_view(), name='editadd'),
    path('personal', EditInfo.as_view(), name='editinfo'),
    path('changeinfo', ChangeInfo.as_view(), name='changeinfo'),
    path('visit', getPerson.as_view(), name='getperson'),
    path('message', Message.as_view(), name='getmessage'),
    path('changeimage', changeimage, name='changeimage'),
    path('visitmessage', Message.as_view(), name='visitmessage'),
    url(r'^detail/(\d+)/$', get_details, name='blog_get_detail'),
    url(r'^search/$', search, name='search'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

]