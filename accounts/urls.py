from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView

urlpatterns = [
    path('profile/<int:user_pk>/', login_required(views.profile), name='profile'),
    path('', include('allauth.urls')),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update')
]