from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    re_path(r'^profile/(?P<pk>[0-9]+)/$', login_required(views.ProfileView.as_view()), name='profile'),
    path('', include('allauth.urls')),
    path('login/', views.login),
]