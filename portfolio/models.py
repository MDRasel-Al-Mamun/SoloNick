from django.db import models
from django.utils.safestring import mark_safe
from tinymce import HTMLField
from django.urls import reverse


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
        return reverse('portfolio_category', kwargs={'id': self.id, 'slug': self.slug})


class Portfolio(models.Model):

    OPTIONS = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    client = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    thumbnail = models.FileField(upload_to='portfolio/thumbnail/%Y/%m/%d')
    video = models.FileField(blank=True, upload_to='portfolio/video/%Y/%m/%d')
    image_caption = models.CharField(max_length=100, default='Photo by Portfolio')
    locatiion = models.CharField(max_length=100)
    locatiion_map = models.URLField(null=True, blank=True)
    topic = models.CharField(max_length=50)
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default='draft')
    read = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title

    def thumbnail_tag(self):
        if self.thumbnail.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.thumbnail.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('portfolio_details', kwargs={'id': self.id, 'slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url


class Details(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    detail = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Details"

    def __str__(self):
        return self.title


class Images(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(
        blank=True, upload_to='portfolio/images/%Y/%m/%d')

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
