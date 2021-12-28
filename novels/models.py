from django.db import models
import datetime
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db.models.aggregates import Count
from profiles.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify, title
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
User = get_user_model()

# Generate unique slug
def unique_slug(title):
    uniqueid = uuid.uuid1().hex[:3]                
    slug = slugify(title) + "-" + str(uniqueid)

    if not Novel.objects.filter(slug=slug).exists():
        # If there's no posts with such slug,
        # then the slug is unique, so I return it
        return slug
    else:
        # If the post with this slug already exists -
        # I try to generate unique slug again
        return unique_slug(title)


class Authors(models.Model):
    author=models.CharField(max_length=50,blank=True)
    slug=models.SlugField(max_length=50,default='')
    def __str__(self):
        return self.author
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.author)
        super(Authors, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return ('view_author', None, {'slug': self.slug })

class Status(models.Model):
    status=models.CharField(max_length=40)
    slug=models.SlugField(max_length=50,default='')
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.status)
        super(Status, self).save(*args, **kwargs)
    def __str__(self):
        return self.status
    def get_absolute_url(self):
        return ('view_author', None, {'slug': self.slug })



class Novel(models.Model):
    title=models.CharField(max_length=255,unique=True,null=True)
    slug = models.SlugField(max_length=64, default="")
    sub = models.CharField(max_length=50, blank=True)
    author=models.ForeignKey(Authors,on_delete=models.PROTECT,null=True,related_name='author_novel')
    status=models.ForeignKey(Status, on_delete=models.PROTECT,null=True,related_name='status_novel')
    cover=models.ImageField(upload_to='images/',null=True)
    description= models.CharField(max_length=500, null=True)
    sumary=models.CharField(max_length=1000,blank=True, null=True)
    category = models.ManyToManyField('categories.Category',
                                  related_name="posts",
                                  blank=True, )  
    tags=models.ManyToManyField('tags.Tag',related_name='novels',blank=True)
    rank=models.PositiveIntegerField(null=True, blank=True , default=0)
    novel_views=models.IntegerField (default=0, blank=True, null=True)
    book_marked = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='book_marked', blank=True) # many 
    average = models.DecimalField(blank=True,decimal_places=1,max_digits=2,null=True,default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    created =models.DateField(auto_now_add=True)
    update_at= models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Novels'
       # constraints = (
        #    models.UniqueConstraint(
         #       fields = ('slug', ),
          #      include = ('title')
           # )
        #)
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title
    
    @property
    def count(self):
        review = Review.objects.filter(novel =self.id).aggregate(review =Count('review'))
        chapter = NovelChapter.objects.filter(novel = self.id).aggregate(chapter = Count( 'chapter'))
        return chapter ,review
    

    def save(self,*args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
           "notification_broadcast",
            {
            'type': 'send_notification',
            'message': json.dumps(f'Realised or update {self.novel}')
            }
         )
        super().save(*args, **kwargs)

    def save(self, slug="", *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Novel, self).save(*args, **kwargs) 
    @classmethod
    def update_avg(cls, novel_id, avg,views):
        Novel.objects.filter(id = novel_id).update(average=avg,novel_views= views+1)

class Review(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='review')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='profile_review')
    review = models.TextField(max_length=660)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='reviews', blank=True) # many 

    def __str__(self):
        return f'{self.novel} - {self.added_by}'

    @staticmethod
    def create_review(novel, added_by,profile,review,rating):
        reviews = Review()
        reviews.novel = novel
        reviews.added_by = added_by
        reviews.profile = profile
        reviews.review = review
        reviews.rating = rating
        reviews.save()
        return reviews



        

class Comment(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='comments')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='comments')
    body = models.TextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comments', blank=True) # many 

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return '%s - %s' % (self.body[:50], self.added_by)
    # pass

class Reply_Comment(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="reply_comments")
    added_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='reply_comments')
    reply=models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reply_comments', blank=True) # many 

    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return '%s - %s' % (self.reply[:50], self.added_by)

class Reply_Review(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name="reply_review")
    added_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='comment_reply_review')
    reply=models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reply_reviews', blank=True) # many 

    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return '%s - %s' % (self.reply[:50], self.added_by)
        
class NovelChapter(models.Model):
    novel=models.ForeignKey(Novel,on_delete=models.CASCADE,null=True,related_name="novel_chapter")
    title=models.CharField(null=True, max_length=255)
    slug = models.SlugField(max_length=100, null=True)
    chapter=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,editable=False)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=("created_at",)
        
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(NovelChapter, self).save(*args, **kwargs)

        
    def get_absolute_url(self):
        return ('view_tag', None, {'slug': self.slug })

    def save(self,*args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
           "notification_broadcast",
            {
            'type': 'send_notification',
            'message': json.dumps(f'Realised or update chapter {self.title}')
            }
         )
        super().save(*args, **kwargs)


            
class LibraryManager(models.Manager):
    def check_product(self, user, product_id):
        if user.is_authenticated:
            return user.favorite_products.products.filter(id=product_id).exists()



class Library(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, related_name='favorite_products')
    products = models.ManyToManyField(
        Novel, related_name='products', blank=True)

    objects = LibraryManager()

    class Meta:
        verbose_name_plural = 'Favorites Librarys'

    def __str__(self):
        return self.user.username

    @property
    def products_count(self):
        return self.products.all().count()

    # Each user should be have favorite products
# When user registered create favorite products model with this user


@receiver(post_save, sender=User)
def create_fvorite_products(sender, instance, created, **kwargs):
    if created:
        Library.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_fvorite_products(sender, instance, **kwargs):
    instance.favorite_products.save()   
    
