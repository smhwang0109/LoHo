from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/<int:user_pk>/', login_required(views.profile), name='profile'),
    path('', include('allauth.urls')),
    path('login/', views.login, name='login'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update')
]