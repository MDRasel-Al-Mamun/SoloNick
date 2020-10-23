from django.shortcuts import render, get_object_or_404
from portfolio.models import Portfolio
from myProfile.models import *


def homeView(request):
    page = 'home'
    projects = Portfolio.objects.filter(status='Published').order_by('-id')[:10]
    profile = get_object_or_404(MyProfile)
    services = Service.objects.filter(status='True').order_by('id')[:4]
    resumes = Resume.objects.filter(status='True').order_by('id')[:6]
    presentation = get_object_or_404(Presentation)
    context = {
        'page': page,
        'projects': projects,
        'profile': profile,
        'services': services,
        'resumes': resumes,
        'presentation': presentation
    }
    return render(request, 'home/index.html', context)


def servicesView(request):
    services = Service.objects.filter(status='True').order_by('id')
    context = {
        'services': services,
    }
    return render(request, 'home/services.html', context)


def contactView(request):
    context = {}
    return render(request, 'home/contacts.html', context)
