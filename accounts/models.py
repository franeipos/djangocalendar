from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

User._meta.get_field('email').blank = False


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=30, blank=True)


# Methods executed when the signal of user create or update are triggered.
@receiver(post_save, sender=User)
def create_user_therapist(sender, instance, created, **kwargs):
    if created:
        Therapist.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_therapist(sender, instance, **kwargs):
    instance.therapist.save()
