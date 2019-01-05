from django.contrib import admin
from bloginfo.models import Category, Tag, BlogInfo, Comment



admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BlogInfo)
admin.site.register(Comment)