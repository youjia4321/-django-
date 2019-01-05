from django import forms


class AddForm(forms.Form):
    title = forms.CharField(label='标题', error_messages={'required': '请填写标题'})
    author = forms.CharField(label='作者', error_messages={'required': '请填写作者'})
    content = forms.CharField(label='博客内容', error_messages={'required': '请填写正文'})
    category = forms.CharField(label='类别', error_messages={'required': '请填写类别'})
    tag = forms.CharField(label='标签', error_messages={'required': '请填写标签'})


class CommentForm(forms.Form):
    email = forms.EmailField(label='邮箱',error_messages={
        'required':'请填写您的邮箱',
        'invalid':'邮箱格式不正确'
    })
    content = forms.CharField(label='内容',max_length=300, error_messages={
        'required':'请填写您的评论内容!',
        'max_length':'评论内容太长咯'
    })
