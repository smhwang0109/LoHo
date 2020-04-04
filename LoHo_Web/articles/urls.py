from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('detail/', views.ArticleDetailView.as_view()),
    path('upload/', views.ArticleCreateUpdateView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)