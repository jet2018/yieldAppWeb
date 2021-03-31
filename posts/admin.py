from django.contrib import admin
from .models import postComment, Post, Commentreply
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "posted_by", "posted_on", "total_likes", "total_comments")
	list_filter = ("posted_on", "posted_by")
class postCommentAdmin(admin.ModelAdmin):
	list_display = ("comment_to", "comment_by", "total_likes", "comment_on")

class CommentreplyAdmin(admin.ModelAdmin):
	list_display = ("reply_to", "reply_by", "total_likes", "reply_on")
	
admin.site.register(Post, PostAdmin)
admin.site.register(postComment, postCommentAdmin)
admin.site.register(Commentreply, CommentreplyAdmin)
