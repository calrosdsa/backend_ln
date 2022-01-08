from django.db import models
from django.conf import settings
from django.utils import tree # you can use this for models instead of CustomUser
from django.contrib.contenttypes.models import ContentType      
from django.contrib.contenttypes.fields import GenericForeignKey
from .signals import object_viewed_signal
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='profile') # null = True means that the CustomUser doesnt need to have a Profile model
    name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='images/')
    bio = models.TextField(null=True)
    def __str__(self):
        return str(self.user)


class HistoryNovel(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    novel  = models.ForeignKey('novels.Novel',on_delete=models.CASCADE) # is the actual object
    viewed_on       = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.novel.title

class History(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True) # product, post
    object_id       = models.PositiveIntegerField() # 1,2,3
    content_object  = GenericForeignKey() # is the actual object
    viewed_on       = models.DateTimeField(auto_now_add=True)
    title = models.CharField()

    def __str__(self):
        return "%s viewed: %s" %(self.content_object, self.viewed_on)

    class Meta:
        verbose_name_plural = "Histories"
        ordering=("-viewed_on",) 

    @property
    def title(self):
        return self.content_object.title

    @property
    def cover(self):
        return self.content_object.cover
    
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    
    History.objects.update_or_create(
        user    = request.user,
        content_type    = ContentType.objects.get_for_model(sender),
        object_id      = instance.id,
    )

object_viewed_signal.connect(object_viewed_receiver)