from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:article_id>/', views.ArticleDetailView.as_view(), name='detail'),
    path('upload/', views.ArticleCreateUpdateView.as_view(), name='upload'),
    path('<int:article_id>/comment_upload/', views.comment_upload, name='comment_upload'),
    path('<int:article_id>/man_participation/', views.man_participation, name='man_participation'),
    path('<int:article_id>/woman_participation/', views.woman_participation, name='woman_participation'),
    path('list/<str:category>/', views.category_list, name='category_list'),
    path('search/', views.search, name='search'),
]

