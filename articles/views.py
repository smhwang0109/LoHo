from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from django.contrib.auth.models import User
from .models import Article
from .forms import UploadForm
from datetime import datetime

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
        ctx = {
            'article': article,
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
