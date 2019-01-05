from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    image = models.ImageField(upload_to="person" , default='person/default.jpg', max_length=100, verbose_name='用户头像')
    mood = models.CharField(max_length=300, verbose_name='个性签名', default="暂无签名")
    visit = models.IntegerField(default=0, verbose_name='访问量')
    gender = models.CharField(max_length=6, choices=(('男', '男'), ('女', '女')), default='female', verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailCodeRecord(models.Model):
    code = models.CharField(max_length=25, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型', max_length=10, choices=(('register', '注册'), ('forget', '忘记密码')))
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class MessageModel(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE) 
    name = models.CharField(verbose_name='称呼',max_length=200)
    content = models.CharField(verbose_name='内容',max_length=240)
    pub = models.DateTimeField(verbose_name='发布时间',default=datetime.now)

    class Meta:
        verbose_name = "留言信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)
