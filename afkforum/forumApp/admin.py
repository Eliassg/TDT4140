from django.contrib import admin
from .models import Post, Comment, Emne, ReportPost, ReportComment

from django.urls import reverse
from django.utils.safestring import mark_safe


class ReportPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_link')
    read_only_fields = ('post_link',)

    def post_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:forumApp_post_change", args=(obj.post.pk,)),
            obj.post.__str__()
        ))

    post_link.short_description = 'post'


class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment_link')
    read_only_fields = ('comment_link',)

    def comment_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:forumApp_comment_change", args=(obj.comment.pk,)),
            obj.comment.__str__()
        ))

    comment_link.short_description = 'comment'



admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Emne)
admin.site.register(ReportPost, ReportPostAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)