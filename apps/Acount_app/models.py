from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='ایمیل',
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    username = models.CharField(max_length=100, verbose_name="نام کاربری",blank=False,null=True,unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    image = models.ImageField(upload_to="user/image",
                             verbose_name="تصویر پروفایل",null=True,blank=True)
    is_teacher = models.BooleanField(default=False, verbose_name="مدرس هست یا خیر؟")
    is_active = models.BooleanField(default=True, verbose_name="کاربر فعال هست یا خیر؟")
    is_admin = models.BooleanField(default=False, verbose_name="کاربر ادمین هست یا خیر؟")
    full_name = models.CharField(max_length=50,null=True,blank=True, verbose_name="نام و نام خانوادگی")
    special_user = models.DateTimeField(default=timezone.now(), verbose_name="کاربر خاص تا زمان:")

    class Meta:
        verbose_name_plural = "حساب های کاربری"
        verbose_name = "حساب کاربری"

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'

    def _str_(self):
        return self.phone_number or self.email

    def is_specialuser(self):
        if self.special_user > timezone.now():
            return True
        return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Techer(models.Model):

    p=[
        ("توسعه دهنده بک اند","توسعه دهنده بک اند"),
        ("مدرس","مدرس"),
        ("توسعه دهنده فرانت اند","توسعه دهنده فرانت اند"),
        ("مدرس و توسعه دهنده","مدرس و توسعه دهنده"),
        ("مدیر وبسایت","مدیر وبسایت"),
        (" امنیت و شبکه","امنیت و شبکه"),
        ("توسعه دهنده فلاتر","توسعه دهنده فلاتر"),
        ("توسعه دهنده بلاکچین","توسعه دهنده بلاکچین"),
        ("توسعه دهنده موبایل","توسعه دهنده موبایل"),
        ("برنامه نویس","برنامه نویس"),
        ("متخصص سئو","متخصص سئو"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="teacher", verbose_name="نام کاربری")
    about_me = models.TextField(verbose_name="بیوگرافی")
    followers = models.ManyToManyField(User, related_name="followers", null=True, blank=True,
                                       verbose_name="دنبال کننده ها")
    slug = models.SlugField(null=True, blank=True, allow_unicode=True,verbose_name="نام و نام خانوادگی")
    resume = models.FileField(upload_to="teacher/cv", null=True, blank=True, verbose_name="رزومه")
    is_active = models.BooleanField(default=False, verbose_name="مدرس فعال هست یا حیر؟")
    position=models.CharField(choices=p,blank=True,null=True,max_length=50,verbose_name="چه جایگاهی در سایت دارد؟")
    instagram=models.CharField(max_length=200,default="https://www.instagram.com/")
    github=models.CharField(max_length=200,default="https://www.github.com/")
    linkedin=models.CharField(max_length=200,default="https://www.linkedin.com/")
    twitter=models.CharField(max_length=200,default="https://twitter.com/")

    class Meta:
        verbose_name_plural = "مدرس ها"
        verbose_name = "مدرس"

    def save(self, *args, **kwargs):

        self.slug = slugify(self.user.full_name, allow_unicode=True)

        super(Techer, self).save(*args, **kwargs)

    def get_absolut_url(self):

        return reverse("Acount_app:profile_teacher", kwargs={"pk": self.id})

    def teacher_active(self):

        if self.is_active == True:

            return True
        else:
            return False

    def __str__(self):
        return self.user.username


class Otc(models.Model):
    phone=models.CharField(max_length=15,verbose_name="شماره تلفن")
    code=models.CharField(max_length=5,verbose_name="کد اعتبارسنجی")
    token=models.CharField(max_length=50,verbose_name="توکن اعتبار سنجی")
    expiration_date=models.DateTimeField(default=(timezone.now()+timezone.timedelta(minutes=10)),verbose_name="تاریخ انقضای کد اعتبار سنجی")

    def is_expiration_date(self):

        if self.expiration_date >= timezone.now():
            return True
        else:
            return False

    def __str__(self):

        return self.phone

    class Meta:
        verbose_name_plural="کدهای اعتبارسنجی"
        verbose_name="کد اعتبارسنجی"


