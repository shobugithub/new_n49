from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import MyUserManager as UserManager


class User(AbstractUser):
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    username = models.CharField(
        'Username', max_length=100, null=True, blank=True)
    email = models.EmailField('Email', max_length=100, unique=True)
    bio = models.TextField('About', null=True, blank=True)
    profile_image = models.ImageField('Profile image',
                                      default='profile-images/user-default.png',
                                      upload_to='profile-images/',
                                      null=True, blank=True)
    location = models.CharField(
        'Location', max_length=100, null=True, blank=True)
    occupation = models.CharField(
        'Occupation', max_length=200, null=True, blank=True)
    social_telegram = models.URLField(
        'Telegram', max_length=200, null=True, blank=True)
    social_instagram = models.URLField(
        'Instagram', max_length=200, null=True, blank=True)
    social_facebook = models.URLField(
        'Facebook', max_length=200, null=True, blank=True)
    social_twitter = models.URLField(
        'Twitter', max_length=200, null=True, blank=True)
    social_whatsapp = models.URLField(
        'Whatsapp', max_length=200, null=True, blank=True)
    social_linkedin = models.URLField(
        'LinkedIn', max_length=200, null=True, blank=True)
    social_youtube = models.URLField(
        'YouTube', max_length=200, null=True, blank=True)
    social_github = models.URLField(
        'GitHub', max_length=200, null=True, blank=True)
    social_website = models.URLField(
        'Website', max_length=200, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)


class Skill(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.owner} - {self.name}'
