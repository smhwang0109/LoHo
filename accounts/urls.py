from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    re_path(r'^profile/(?P<pk>[0-9]+)/$', login_required(views.ProfileView.as_view()), name='profile'),
    path('', include('allauth.urls')),
    path('login/', views.login),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update')
]