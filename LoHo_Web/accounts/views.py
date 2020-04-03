from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

# Create your views here.
class ProfileView(DetailView):
    context_object_name = 'profile_user' # model로 지정해준 User모델에 대한 객체와 로그인한 사용자랑 명칭이 겹치기 때문에 이를 지정해줌.
    model = User
    template_name = 'accounts/profile.html'