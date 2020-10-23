from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count



class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'id': self.id, 'slug': self.slug})


class Post(models.Model):

    OPTIONS = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    title = models.CharField(max_length=300)
    overview = models.TextField(null=True)
    thumbnail = models.FileField(upload_to='blog/posts/%Y/%m/%d')
    image_caption = models.CharField(max_length=100, default='Photo by Blog')
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    tags = TaggableManager()
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default='draft')
    read = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def datepublished(self):
        return self.publish_date.strftime('%d %B %Y')

    def thumbnail_tag(self):
        if self.thumbnail.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.thumbnail.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'id': self.id, 'slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url
    
    @property
    def countreview(self):
        comment = Comment.objects.filter(post=self).aggregate(count=Count('id'))
        cnt = 0
        if comment["count"] is not None:
            cnt = int(comment["count"])
        return cnt


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d')

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def children(self):
        return Comment.objects.filter(reply=self)
