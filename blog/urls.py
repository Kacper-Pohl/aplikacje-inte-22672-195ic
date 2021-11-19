from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    path('', views.base, name='base'),
    url(r'^$', views.base, name='home'),
    url(r'^password_change/$', views.change_password, name='change_password'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/reset_password/$', auth_views.PasswordResetView.as_view(template_name = "registration/reset_password.html"),name ='reset_password'),
    url(r'^accounts/password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name = "registration/password_reset_sent.html"), name ='password_reset_done'),
    url(r'^accounts/reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"), name ='password_reset_complete'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_form.html"), name ='password_reset_confirm'),
]