from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'homepage', 'created_at', 'parent')
    ordering = ('-created_at', '-username')


admin.site.register(Comment, CommentAdmin)
