from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin \
    , BaseUserManager
from datetime import datetime
from store.models import Cart


# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        '''
        根据用户名和密码创建一个用户
        '''
        now = datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    reset_password_token = models.CharField(max_length=40, blank=True, null=True)
    reset_password_token_create_time = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar/', default = '/avatar/avatar.png')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    sign = models.CharField(max_length=100, blank=True, null=True)
    address_info = models.ManyToManyField('Address')
    cart = models.ForeignKey(Cart)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return self.user.username

class Address(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    detail_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
