from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views import View
from .forms import UserForm, ProfileForm
from allauth.socialaccount.models import SocialAccount

# Create your views here.
def profile(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    if hasattr(profile_user, 'profile'):
        if profile_user.profile.gender == '남':
            participations = profile_user.manparticipation_set.all
        else:
            participations = profile_user.womanparticipation_set.all
    else:

        participations = '프로필 수정 필요'
    socialaccount = get_object_or_404(SocialAccount, user=profile_user)
    if socialaccount.provider == 'naver':
        pass
    elif socialaccount.provider == 'kakao':
        if socialaccount.extra_data['kakao_account']['has_gender']:
            if not socialaccount.extra_data['kakao_account']['gender_needs_agreement']:
                socialaccount.extra_data['kakao_account']['gender']
    elif socialaccount.provider == 'facebook':
        pass
    context = {
        'socialaccount' : socialaccount,
        'profile_user': profile_user,
        'participations':participations,
    }
    return render(request, 'account/profile.html', context)

class ProfileUpdateView(View):
    def get(self, request):
        profile_user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'username': profile_user.username,
        })

        if hasattr(profile_user, 'profile'):
            profile = profile_user.profile
            profile_form = ProfileForm(instance=profile)
        else:
            profile_form = ProfileForm()

        return render(request, 'account/profile_update.html', {"user_form":user_form, "profile_form":profile_form})

    def post(self, request):
        profile_user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(request.POST, instance=profile_user) # 기존의 것의 업데이트 하는 것 이므로 기존의 인스턴스를 넘겨줘야 한다. 기존의 것 가져와 수정하는 것

        if user_form.is_valid():
            user_form.save()

        if hasattr(profile_user, 'profile'):
            profile = profile_user.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # 기존 것 가져오는게 아니고 새로 만들 경우 user를 지정해줘야 한다.
            profile.user = profile_user
            profile.save()

        return redirect('profile', request.user.pk)