from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

from .models import Project, Tag, Message
from .forms import ProjectForm, MessageForm


User = get_user_model()

class CustomRangeForPagination:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1
        
        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context


class DevelopersView(CustomRangeForPagination, ListView):
    template_name = 'app_main/developers.html'
    paginator_class = Paginator
    paginate_by = 2

    def get_queryset(self):
        return User.objects.all()
    context_object_name = 'developers'


class ProjectsView(CustomRangeForPagination, ListView):
    model = Project
    template_name = 'app_main/projects.html'
    context_object_name = 'projects'
    paginator_class = Paginator
    paginate_by = 2



class ProjectCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = Project
    template_name = 'app_main/project_form.html'
    form_class = ProjectForm
    extra_context = {
        'btn_text': 'Create project'
    }

    def get_success_url(self):
        return reverse('account', kwargs={'user_id': self.request.user.id})

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            tags = self.request.POST.get('tags', '').split(',')
            project_form = ProjectForm(self.request.POST)

            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.owner = self.request.user
                project.save()

                # Process and add tags
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.strip())
                    project.tags.add(tag.lower())

                project.save()  # Final save with tags
                return redirect("account", user_id=self.request.user.id)

            # If form is invalid, render the form with errors
            return redirect("project_create", kwargs={'user_id': self.request.user.id})

        return super().dispatch(request, *args, **kwargs)


class ProjectDetail(DetailView):
    model = Project
    pk_url_kwarg = 'project_id'
    template_name = 'app_main/project.html'


class ProfileView(DetailView):
    model = User
    pk_url_kwarg = 'user_id'
    template_name = 'app_main/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['dev_skills'] = self.get_object(
        ).skill_set.exclude(description="")
        context['other_skills'] = self.get_object(
        ).skill_set.filter(description="")
        return context


def handle_message_submission(request, receiver_id):
    form = MessageForm(request.POST or None)

    if request.user.is_authenticated:
        form.fields.pop('fullname', None)
        form.fields.pop('email', None)

    if request.method == 'POST':

        if form.is_valid():
            message = form.save(commit=False)

            if request.user.is_authenticated:
                message.sender = request.user
                message.fullname = request.user.fullname
                message.email = request.user.email

            # Retrieve the receiver user with error handling
            message.receiver = get_object_or_404(User, id=receiver_id)
            message.save()
            return redirect('profile_detail', user_id=receiver_id)

    print(form.fields)
    context = {
        'form': form,
        'btn_text': _('Send message')
    }
    return render(request, 'form.html', context)



class InboxView(ListView):
    queryset = Message.objects.all().order_by('is_read', '-created')
    template_name = 'app_main/inbox.html'
    context_object_name = 'messages'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['unread_messages_count'] = Message.objects.filter(is_read=False).count()
        return context

class MessageView(DetailView):
    model = Message
    template_name = 'app_main/message.html'
    context_object_name = 'message'
    pk_url_kwarg = 'message_id'

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_read = True
        message.save()
        return super().dispatch(request, *args, **kwargs)
