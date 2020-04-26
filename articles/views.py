from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from django.contrib.auth.models import User
from .models import Article, Comment
from .forms import UploadForm, CommentForm
from datetime import datetime

from django.db.models import Avg

class IndexView(TemplateView):    # 게시글 목록
    template_name = 'articles/index.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()  # 모든 게시글
        ctx = {
            'articles': articles, # 검색 결과
        }  # 템플릿에 전달할 데이터
        return self.render_to_response(ctx)



class ArticleDetailView(TemplateView):  # 게시글 상세
    template_name = 'articles/article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'  # 검색 데이터의 primary key를 전달받을 이름

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset  # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs)  # pk는 모델에서 정의된 pk값, 즉 모델의 id
        article = queryset.filter(pk=pk).first()  # pk로 검색된 데이터가 있다면 그 중 첫번째 데이터가 없다면 None 반환

        if not article:
            raise Http404('invalid pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        comments_aggregate = Comment.objects.aggregate(Avg('rank'))
        comment_form = CommentForm()
        ctx = {
            'article': article,
            'comments_rank_avg': comments_aggregate['rank__avg'],
            'comment_form': comment_form,
        }
        return self.render_to_response(ctx)


class ArticleCreateUpdateView(LoginRequiredMixin, TemplateView):  # 게시글 추가, 수정
    login_url = settings.LOGIN_URL
    template_name = 'articles/article_upload.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'
    

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()
        if pk:
            if not article: # 검색 결과가 없으면 곧바로 에러 발생
                raise Http404('invalid pk')
            elif article.author != self.request.user:  # 작성자 수정하려는 사용자와 다른 경우
                raise Http404('invalid user')
        return article

    def get(self, request, *args, **kwargs):  # 화면 요청
        article = self.get_object()
        form = UploadForm(instance=article)
        ctx = {
            'article': article,
            'form':form
        }
        return self.render_to_response(ctx)

    def post(self, request):  # 액션 (서버에 저장)
        action = request.POST.get('action')  # request.POST 객체에서 데이터 얻기
        
        post_data = {key: request.POST.get(key) for key in ('title', 'content', 'price', 'participation', 'man_count', 'woman_count', 'event_date', 'category')}  # 작성자를 입력 받지 않도록 수정
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger')  # error 레벨로 메시지 저장

        if len(messages.get_messages(request)) == 0:
            if action == 'create':
                form = UploadForm(request.POST, request.FILES)
            elif action == 'update':
                article = self.get_object()
                form = UploadForm(request.POST, request.FILES, instance=article)
            else:
                messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')  # error 레벨로 메시지 저장
            
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                messages.success(self.request, '게시글이 저장되었습니다.')  # success 레벨로 메시지 저장
                return HttpResponseRedirect('/articles/')  # 저장 완료되면 '/articles/로 이동됨'

        ctx = {
            'article': self.get_object() if action == 'update' else None,
        }
        return self.render_to_response(ctx)

@require_POST
@login_required
def comment_upload(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.article = article
        comment.save()
    return redirect('articles:detail', article.pk)

@require_POST
@login_required
def man_participation(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user.profile.gender == '여':
        return redirect('articles:woman_participation', article_id)
    if article.man_participations_count >= article.participations:
        messages.error(request, '인원 초과입니다.')
        return redirect('articles:detail', article_id)
    article_manparticipation, article_manparticipation_created = article.manparticipation_set.get_or_create(user=request.user)

    if not article_manparticipation_created:
        messages.error(request, '이미 신청하셨습니다.')
        return redirect('articles:detail', article_id)
    return redirect('articles:detail', article.pk)

@require_POST
@login_required
def woman_participation(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user.profile.gender == '남':
        return redirect('articles:man_participation', article_id)
    if article.woman_participations_count >= article.participations:
        messages.error(request, '인원 초과입니다.')
        return redirect('articles:detail', article_id)
    article_womanparticipation, article_womanparticipation_created = article.womanparticipation_set.get_or_create(user=request.user)

    if not article_womanparticipation_created:
        messages.error(request, '이미 신청하셨습니다.')
        return redirect('articles:detail', article_id)
    return redirect('articles:detail', article.pk)


