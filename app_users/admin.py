from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .models import Skill


User = get_user_model()

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Skill)
