from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .models import Skill
from .forms import UserRegistrationForm, SkillForm, AccountForm

User = get_user_model()


class UserRegistrationView(CreateView):
    model = User
    template_name = 'app_users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return redirect('login')


class AccountView(DetailView):
    model = User
    template_name = 'app_users/account.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'account'


class CreateSkillView(CreateView):
    template_name = 'form.html'
    model = Skill
    form_class = SkillForm

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.owner = self.request.user
        skill.save()
        return redirect('account', user_id=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = _('Create skill')
        return context

    def get_success_url(self) -> str:
        return reverse('account', user_id=self.request.user.id)


class UpdateSkillView(UpdateView):
    template_name = 'form.html'
    model = Skill
    form_class = SkillForm
    pk_url_kwarg = 'skill_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = _('Update skill')
        return context

    def get_success_url(self):
        return reverse('account', kwargs={'user_id': self.request.user.id})


class DeleteSkillView(DeleteView):
    model = Skill
    template_name = 'delete.html'
    pk_url_kwarg = 'skill_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['confirmation_text'] = _(f'Are you sure to delete "{
                                         self.get_object().name}" ?')
        return context

    def get_success_url(self):
        return reverse('account', kwargs={'user_id': self.request.user.id})


class UpdateAccount(UpdateView):
    template_name = 'form.html'
    model = User
    form_class = AccountForm
    pk_url_kwarg = 'user_id'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = _('Update account')
        return context

    def get_success_url(self):
        return reverse('account', kwargs={'user_id': self.request.user.id})



