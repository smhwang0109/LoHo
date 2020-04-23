from django.contrib import admin
from .models import Article, Comment

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank', 'content', 'created_at', 'updated_at', 'author')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)

