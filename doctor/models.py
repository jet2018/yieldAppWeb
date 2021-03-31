from django.db import models
from django.contrib.auth.models import User
from profiler.models import Profile

# Create your models here.

class Notifications(models.Model):
    to = models.ForeignKey(Profile, related_name = "receiver", on_delete=models.CASCADE)
    fro = models.ForeignKey(Profile, related_name = "sender", on_delete=models.CASCADE)
    body = models.TextField(max_length = 1000)
    status = models.BooleanField(default = False)
    sent_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.fro.user.username

    @property
    def total_replies(self):
        return Reply.objects.filter(on = self).count()
    

class Reply(models.Model):
    to = models.ForeignKey(Profile, related_name="receive", on_delete=models.CASCADE)
    fro = models.ForeignKey(Profile, related_name="send", on_delete=models.CASCADE)
    on = models.ForeignKey(Notifications, related_name="notification", on_delete = models.CASCADE)
    body = models.TextField(max_length=1000)
    status = models.BooleanField(default=False)
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fro.user.username

