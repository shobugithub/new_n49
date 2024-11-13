from django.urls import path

from . import views


urlpatterns = [
    path('', views.DevelopersView.as_view(), name='developers'),

    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('project-create/', views.ProjectCreate.as_view(), name='project_create'),
    path('project/<int:project_id>', views.ProjectDetail.as_view(), name='project_detail'),
    
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile_detail'),
    path('send-message/<int:receiver_id>', views.handle_message_submission, name='send_message'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('message/<int:message_id>/', views.MessageView.as_view(), name='message'),
]
