from django.db import models
from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser, User
from django.core.validators import validate_image_file_extension, FileExtensionValidator, validate_email, validate_slug, URLValidator
# from django.core.mail import send_mail

class Post(models.Model):
	"""docstring for Post"""
	title = models.CharField(max_length = 255)
	body = models.TextField()
	video = models.FileField( upload_to='post_videos',validators=[FileExtensionValidator(allowed_extensions=['mpeg', 'mp4', 'webm'], message="Videos have been limited to mp4,mpeg and webm only") ], blank=True, null=True)
	posted_on = models.DateTimeField(auto_now_add = True)
	Image = models.ImageField(upload_to ='post_images', blank=True, null=True,
										validators=[validate_image_file_extension])
	posted_by = models.ForeignKey(User, on_delete = models.CASCADE)
	likes = models.ManyToManyField(User, verbose_name='Likes', related_name='Likes', blank=True)

	def __str__(self):
		return self.title

	@property
	def total_likes(self):
		return self.likes.count()

	@property
	def total_comments(self):
		return postComment.objects.filter(comment_to=self).count()

	def __unicode__(self):
		return u'%s' % self.title

class postComment(models.Model):
	comment_to = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment_by = models.ForeignKey(User, related_name='commenter', on_delete=models.CASCADE)
	comment_body = models.TextField(max_length=650)
	comment_on = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, verbose_name='Likes', related_name='likecomment', blank=True)

	def __str__(self):
		return self.comment_to.title

	@property
	def total_likes(self):
		return self.likes.count()

	@property
	def all_likes(self):
		return self.likes
		
	@property
	def total_replies(self):
		return Commentreply.objects.filter(reply_to=self).count()

	def __unicode__(self):
		return u'%s' % self.comment_to.title


class Commentreply(models.Model):
    reply_to = models.ForeignKey(postComment, on_delete=models.CASCADE)
    reply_by = models.ForeignKey(User, related_name = 'replier', on_delete=models.CASCADE)
    reply_body = models.TextField(max_length = 200)
    reply_on = models.DateTimeField(auto_now_add=True)
    likes =models.ManyToManyField(User, verbose_name='Likes', related_name = 'likereply',  blank = True)
    def __str__(self):
        return self.reply_to.comment_to.title

    @property
    def total_likes(self):
        return self.likes.count()

    def __unicode__(self):
        return  u'%s' %self.reply_to.comment_to.title