import datetime
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.utils.text import slugify

# Create your models here.


class Profile(models.Model):
    """Profile as an extension of the User model"""
    roles = [
        ("dr", "Doctor"),
        ("fr", "Farmer"),
    ]
    role = models.CharField(max_length=10, null=True,
                            blank=True, choices=roles)
    address = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=2000, null=True, blank=True)
    years_of_experiance = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    stars = models.ManyToManyField(
        User, verbose_name='stars', related_name='stars', blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=14)
    profile_pik = models.ImageField(
        null=True, blank=True, upload_to="profiles")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_stars(self):
        return self.stars.count()

    def __str__(self):
        return self.user.username


# comment this on first migrations
now = datetime.datetime.now()
expire_after_30 = now + datetime.timedelta(minutes=30.0)
code = str(int(datetime.datetime.timestamp(now)))
# 1629184190
# 1629184202


class GenerateCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(
        unique=True, max_length=100, default=code)
    generated_on = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(default=expire_after_30)
    reason = models.CharField(max_length=100, null=True, blank=True)

# signals


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


@receiver(pre_save, sender=GenerateCodes)
def BeforeCreateResetPasswordToken(sender, instance=None, **kwargs):
    # token =
    pass


@receiver(post_delete, sender=Profile)
def submission_delete(sender, instance, **kwargs):
    instance.profile_pik.delete(False)
