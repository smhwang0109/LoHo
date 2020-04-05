from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('detail/', views.ArticleDetailView.as_view()),
    path('upload/', views.ArticleCreateUpdateView.as_view()),
]

