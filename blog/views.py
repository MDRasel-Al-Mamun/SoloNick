import json
from taggit.models import Tag
from .forms import SearchForm
from django.http import HttpResponse, JsonResponse
from .models import Category, Post, Images, Comment
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from blog.forms import CommentForm
from django.template.loader import render_to_string



def blogPosts(request):
    posts = Post.objects.filter(status='Published').order_by('-id')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }
    return render(request, 'blog/blog.html', context)


def blogDetails(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.read = post.read + 1
    post.save()
    images = Images.objects.filter(post=post)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(
                post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'images': images,
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'blog/blog-single.html', context)


def categoryView(request, id, slug):
    category = get_object_or_404(Category, id=id, slug=slug)
    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    context = {
        'category': category,
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }
    return render(request, 'blog/category.html', context)


def taggedView(request, id, slug):
    tag = get_object_or_404(Tag, id=id, slug=slug)
    posts = Post.objects.filter(tags=tag)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    context = {
        'tag': tag,
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }
    return render(request, 'blog/tags.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.objects.filter(title__icontains=query)
            paginator = Paginator(posts, 5)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)

            if page.has_next():
                next_url = f'?page={page.next_page_number()}'
            else:
                next_url = ''

            if page.has_previous():
                prev_url = f'?page={page.previous_page_number()}'
            else:
                prev_url = ''
            context = {
                'page': page,
                'next_page_url': next_url,
                'prev_page_url': prev_url,
                'query': query,
            }
            return render(request, 'blog/search.html', context)
    return HttpResponseRedirect('blog')
