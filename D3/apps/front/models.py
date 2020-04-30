from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField
from django.core import validators


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("请传入手机号码！")
        if not username:
            raise ValueError("请输入用户名")
        if not password:
            raise ValueError("请输入密码")

        user = self.model(telephone=telephone, username=username, **kwargs)
        # 将用户的密码加密处理之后在存放到数据库中
        user.set_password(password)
        # 注意，一定要保存，否者的话，不会存储到数据库中
        user.save()
        return user

    # 创建普通用户
    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    # 创建超级用户
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    pip install django-shortuuidfield
    """
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=200)
    telephone = models.CharField(max_length=11, validators=[validators.RegexValidator(r"1[345678]\d{9}")], unique=True)
    email = models.EmailField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    #  定义唯一性校验字段
    USERNAME_FIELD = 'telephone'
    # 在验证的时候还需要输入的字段值
    REQUIRED_FIELDS = ['username']
    # 定义email字段，用来给用户发送邮件
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class PhotosModel(models.Model):
    position = models.IntegerField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField()

    class Meta:
        db_table = 'photos'
        ordering = ['-pub_time']


class PersonModelsModel(models.Model):
    pub_time = models.DateTimeField(auto_now_add=True)
    model_url = models.URLField()

    class Meta:
        db_table = 'person_model'
        ordering = ['-pub_time']
