from django.forms import ModelForm

from . import models
from app_users.forms import AddInputClass


class ProjectForm(AddInputClass, ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'description', 'image', 'source_link', 'demo_link']


class MessageForm(AddInputClass, ModelForm):
    class Meta:
        model = models.Message
        fields = ['fullname', 'email', 'subject', 'body']
    
