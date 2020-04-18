from django.urls import path
from . import views
from django.conf import settings

app_name = 'articles'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:article_id>', views.ArticleDetailView.as_view(), name='detail'),
    path('upload/', views.ArticleCreateUpdateView.as_view(), name='upload'),
]

