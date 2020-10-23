from django.shortcuts import get_object_or_404, redirect, render
from portfolio.models import Portfolio
from myProfile.models import *
from .models import Contact
from django.contrib import messages
from django.template.loader import render_to_string
import threading
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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
    profile = get_object_or_404(MyProfile)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        email_subject = 'Contact Message'
        current_site = get_current_site(request)
        email_body = render_to_string('home/contact_email.html', {
            'message': message,
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'domain': current_site.domain,
        })
        email = EmailMessage(
            email_subject,
            email_body,
            email,
            ['djangoprojectbd@gmail.com'],
        )
        EmailThread(email).start()
        messages.success(request, 'Your Message has been send. Please wait for reply')
        return redirect('contacts')
    context = {
        'profile': profile
    }
    return render(request, 'home/contacts.html', context)
