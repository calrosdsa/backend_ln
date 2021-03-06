from django.db import models
from django.template.defaultfilters import slugify

class Tag(models.Model):
    title = models.CharField(max_length=64)    
    description = models.CharField(max_length=500,blank=True)
    slug = models.SlugField(max_length=64, default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)
    
        
    def get_absolute_url(self):
        return ('view_tag', None, {'slug': self.slug })
