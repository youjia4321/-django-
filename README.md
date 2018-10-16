# -django-
下载压缩包,在命令窗口新建一个目录,在此目录下输入pipenv shell(没有pipenv: pip install pipenv),进入虚拟环境,然后pip install 此安装包就能下载项目所需要的库,然后解压安装包运行manage.py文件(python manage.pu runserver)


运行python manage.py runserver前, 要先进行数据库迁移.(python manage.py makemigrations  然后再 python manage.py migrate) 源码用的数据库是postgreSQL数据库,如果你的数据库是其他的,请在blogs的settings文件中修改
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blogs',
        'USER': 'postgres',
        'PSSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
