from django.shortcuts import get_object_or_404, render
from .models import Category, Images, Portfolio, Details


def portfolioProject(request):
    projects = Portfolio.objects.filter(status='Published').order_by('-id')
    categories = Category.objects.filter(status='True').order_by('-id')
    context = {
        'projects': projects,
        'categories': categories,
    }
    return render(request, 'portfolio/portfolio.html', context)


def portfolioDetails(request, id, slug):
    project = get_object_or_404(Portfolio, id=id, slug=slug)
    project.read = project.read + 1
    project.save()
    images = Images.objects.filter(portfolio=project)
    details = Details.objects.filter(portfolio=project)
    context = {
        'project': project,
        'images': images,
        'details': details,
    }
    return render(request, 'portfolio/portfolio-single.html', context)


def categoryView(request, id, slug):
    category = get_object_or_404(Category, id=id, slug=slug)
    projects = Portfolio.objects.filter(category=category)
    context = {
        'category': category,
        'projects': projects,
    }
    return render(request, 'portfolio/category.html', context)
