from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('upload/', views.upload_files, name='upload'),
    path('logout/', views.logout_view, name='logout'),
    path('send_selected/', views.send_selected, name='send_selected'),
    path('send_rejected/', views.send_rejected, name='send_rejected'),
]
