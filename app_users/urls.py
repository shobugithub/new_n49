from django.urls import path
from django.contrib.auth.views import LoginView


from . import views


urlpatterns = [
    path('account/<int:user_id>/', views.AccountView.as_view(), name='account'),
    path('update-account/<int:user_id>/', views.UpdateAccount.as_view(), name='update_account'),
    
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('create-skill/', views.CreateSkillView.as_view(), name='create_skill'),
    path('update-skill/<int:skill_id>/', views.UpdateSkillView.as_view(), name='update_skill'),
    path('delete-skill/<int:skill_id>/', views.DeleteSkillView.as_view(), name='delete_skill'),
]   