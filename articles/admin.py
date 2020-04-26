from django.contrib import admin
from .models import Article, Comment, ManParticipation, WomanParticipation

# Register your models here.

class ManParticipationInline(admin.TabularInline):
    model = ManParticipation

class WomanParticipationInline(admin.TabularInline):
    model = WomanParticipation

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
    list_display_links = ['title', 'content']
    inlines = [ManParticipationInline, WomanParticipationInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank', 'content', 'created_at', 'updated_at', 'author')


