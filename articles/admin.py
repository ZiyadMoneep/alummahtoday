from django.contrib import admin
from .models import Article, Comment, Category


# Register your models here.


class CommentInline(admin.StackedInline):  # new
    model = Comment
    more = 2


# class CommentInline(admin.TabularInline):  # new
#     model = Comment
#     more = 0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)