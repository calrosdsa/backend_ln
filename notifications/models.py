from django.db import models
from novels.models import Novel
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from novels.models import Novel
from django.db.models.signals import m2m_changed, post_save
#from channels.layers import get_channel_layer
import json
from utils.models import Extensions,TimeStampedModel
#from asgiref.sync import async_to_sync

User = get_user_model()

# Create your models here.

class NovelNotifiactions(TimeStampedModel):
    user = models.ManyToManyField(User)
    name = models.CharField(blank=True,null=True,max_length=255)
    novel = models.ForeignKey(Novel,on_delete=models.CASCADE,blank=True,null=True )
    is_seen = models.BooleanField(default=False)

      
    class Meta:
        verbose_name_plural = 'Notifications'
 #   def save(self,*args, **kwargs):
  #      channel_layer = get_channel_layer()
   #     async_to_sync(channel_layer.group_send)(
    #       "notification_broadcast",
     #       {
      #      'type': 'send_notification',
       #     'message': json.dumps(f'Realised or update {self.novel}')
        #    }
         #)
        #super().save(*args, **kwargs)
    @property
    def cover(self):
        return self.novel.cover
    @classmethod
    def is_seen_true(self,is_seen=False):
        notification = NovelNotifiactions()
        notification.is_seen = is_seen
        notification.save()
        return notification
   


@receiver(post_save, sender=Novel)
def novel_notification(sender,instance,created, **kwargs):
    print('sender', sender,'instance',instance,'created',created)
    if created:
        NovelNotifiactions.objects.update_or_create(novel=instance, name=instance.title)