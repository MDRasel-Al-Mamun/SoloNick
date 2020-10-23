from django.db import models
from tinymce import HTMLField
from django.utils.safestring import mark_safe


class MyProfile(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=50, null=True)
    email = models.EmailField(blank=True)
    about_me = models.TextField(max_length=400, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(blank=True, upload_to='profile/avatar', default='profile/user.png')
    cover_image = models.ImageField(blank=True, upload_to='profile/cover', default='profile/bg.jpg')
    birthday = models.DateField('Date of Birth(Year/Month/Day)', auto_now_add=False, auto_now=False, blank=True)
    cv = models.FileField(blank=True, upload_to='profile/cv')
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    skype_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def avatar_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.avatar.url))

    avatar_tag.short_description = 'Avatar'

    @property
    def coverImageURL(self):
        try:
            url = self.cover_image.url
        except:
            url = ''
        return url


class Service(models.Model):
    ICONS = (
        ('desktop', 'Web Design'),
        ('file-code', 'Web Development'),
        ('mobile-android', 'Ui/Ux Design'),
        ('adversal', 'Advetising'),
        ('podium-star', 'Motivational Speak'),
        ('street-view', 'Consultant'),
        ('game-console-handheld', 'Game Development'),
        ('microsoft', 'Softwere Development'),
        ('pencil-paintbrush', 'Graphic design'),
        ('pencil-alt', 'Story Writing'),
    )
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=100, choices=ICONS)
    price = models.CharField(max_length=50, default='0$-0$')
    cover_image = models.ImageField(blank=True, upload_to='services/cover', default='services/cover.jpg')
    details = models.TextField(max_length=400, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def coverImageURL(self):
        try:
            url = self.cover_image.url
        except:
            url = ''
        return url


class Resume(models.Model):
    ICONS = (
        ('university', 'Education'),
        ('briefcase', 'Work'),
    )
    LABEL = (
        ('educ', 'Education'),
        ('workres', 'Work'),
    )
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    institute = models.CharField(max_length=250, null=True, blank=True)
    year = models.CharField(max_length=15, default='2000-2010')
    discription = HTMLField()
    icon = models.CharField(max_length=100, choices=ICONS)
    label = models.CharField(max_length=100, choices=LABEL)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Presentation(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=400, blank=True)
    image = models.ImageField(upload_to='profile/presentation')
    video_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
