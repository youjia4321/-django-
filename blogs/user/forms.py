from django import forms
from captcha.fields import CaptchaField
from user.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=1, error_messages={'required': '请填写用户名', 'max_length':'用户名过长', 'min_length': '用户名过短'})
    password = forms.CharField(label='密码', min_length=6, max_length=20, error_messages={'required': '请填写用密码','max_length':'密码过长', 'min_length': '密码过短'})
    # captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class RegisterForm(forms.Form):
    email = forms.EmailField(label='邮箱', min_length=3, error_messages={'required': '请填写邮箱号', 'min_length': '邮箱过短'})
    username = forms.CharField(label='用户名', min_length=1, error_messages={'required': '请填写用户名', 'max_length':'用户名过长', 'min_length': '用户名过短'})
    password = forms.CharField(label='密码', min_length=6, max_length=20, error_messages={'required': '请填写密码','max_length':'密码过长', 'min_length': '密码过短'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误', 'required': '请填写验证码'})

class ModifyPwdForm(forms.Form):
    email = forms.CharField(label='邮箱', min_length=3, error_messages={'required': '请填写邮箱号', 'min_length': '邮箱过短'})
    password1 = forms.CharField(label="新密码", min_length=6, error_messages={'required': '请填写新密码', 'min_length': '密码过短'})
    password2 = forms.CharField(label="确认密码", min_length=6, error_messages={'required': '请填确认密码', 'min_length': '密码过短'})

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='邮箱', min_length=3, error_messages={'required': '请填写邮箱', 'min_length': '邮箱过短'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误', 'required': '请填写验证码'})

class ChangeInfoForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=1, error_messages={'required': '请填写用户名', 'max_length':'用户名过长', 'min_length': '用户名过短'})
    mood = forms.CharField(label='签名', max_length=200, error_messages={'required': '请填写签名'})
    birthday = forms.DateField(required=True)
    address = forms.CharField(required=True)


class MessageForm(forms.Form):
    message = forms.CharField(label="留言", max_length=200, error_messages={'required': '填写留言内容'})


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']