from django import template
from blog.models import *
from django.db.models import Count
from django.utils import timezone
from myProfile.models import MyProfile
from django.shortcuts import get_object_or_404


register = template.Library()


@register.simple_tag
def profile_sidebar():
    return get_object_or_404(MyProfile)


@register.simple_tag
def popular_sidebar(count=4):
    month = timezone.now() - timezone.timedelta(days=30)
    trends = Post.objects.filter(publish_date__gte=month).order_by('-read')[:count]
    return trends


@register.simple_tag
def category_sidebar(count=6):
    return Category.objects.filter(status='True').order_by('id').annotate(cat_num=Count('post'))[:count]


@register.simple_tag
def tag_sidebar(count=6):
    return Post.tags.most_common()[:count]
