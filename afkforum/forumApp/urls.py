from django.urls import path
from . import views#, settings # settings pga bilder

# Imports for register of user (Baard)
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from django.contrib.staticfiles.urls import static # for bilder

from forumApp import views as forumApp_views
from django.contrib.auth.models import User


from forumApp import forms 




# URL patterns for directing to pages when you login/signup/logout/click home.

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.emneSide, name="enkeltemne"),
    url(r'^$', forumApp_views.index, name='index'),
    url(r'^login/$', forumApp_views.loginPage, name='login'),
    url(r'^logout/$', forumApp_views.logoutUser, name='logout'),
    url(r'^signup/$', forumApp_views.registerPage, name='register'),
    url(r'^postCreation/$', forumApp_views.postCreation, name='postCreation'),
    path('<int:id>/', views.emneSide, name="enkeltemne"),
    path('userpost/<slug:post_id>', views.userpost, name="userpost view"),
    path('userpost/<slug:post_id>/like', views.PostLikeToggle.as_view(), name="like-toggle"),
    url(r'^profile/$', forumApp_views.view_profile, name='profil'),
    url(r'^delete/(?P<username>[\w|\W.-]+)/$', views.delete_user, name='delete_user'),
    url(r'^deleteUser/$', views.delete_user_confirm, name='deleteUser'),
    url(r'^results/$', views.show_search_result, name='results'),
    path('profile/<slug:username>', views.view_profile, name="view_profile"),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change-password/$', views.change_password, name='change_password'),
    url(r'^deleteUser/$', views.delete_user_confirm, name='deleteUser'),
    url(r'^delete/(?P<username>[\w|\W.-]+)/$', views.delete_user, name='delete_user')

]
