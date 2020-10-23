import json
import threading
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .utils import account_activation_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)



class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username is already taken, choose another one'}, status=409)
        if len(username) < 8:
            return JsonResponse({'username_error': 'Your username must consist of at least 8 characters'}, status=400)
        return JsonResponse({'username_valid': True})
        

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email is already taken, choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signup.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'message': first_name + ' ' + last_name,
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    return render(request, 'authentication/signup.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                email_body = render_to_string('authentication/email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'djangoprojectbd@gmail.com',
                    [email],
                )
                EmailThread(email).start()
                return render(request, 'authentication/signup.html', context)
        return render(request, 'authentication/signup.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('signin'+'?message='+'User Already Activated')

            if user.is_active:
                return redirect('signin')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated Successfully')
            return redirect('signin')

        except Exception as ex:
            pass

        return redirect('signin')


class SigninView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signin.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')

        elif not User.objects.filter(username=username).exists():
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('signin')

        elif not User.objects.get(username=username).is_active:
            messages.error(request, 'Account is not active, please check your email')
            return redirect('signin')

        else:
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('signin')

        return render(request, 'authentication/signin.html')


def signoutView(request):
    logout(request)
    messages.success(request, 'You are sign out successfully')
    return redirect('signin')


class RequestPasswordResetEmail(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/password_reset.html')

    def post(self, request):
        email = request.POST['email']
        context = {
            'email': email,
        }
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Please enter your correct email address')
            return render(request, 'authentication/password_reset.html')

        user = User.objects.filter(email=email)
        current_site = get_current_site(request)

        if user.exists():
            email_body = render_to_string('authentication/reset_email.html', {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            })
            email_subject = 'Password Reset Instructions'
            email = EmailMessage(
                email_subject,
                email_body,
                'djangoprojectbd@gmail.com',
                [email],
            )
            EmailThread(email).start()
            return render(request, 'authentication/password_reset.html', context)

        return render(request, 'authentication/password_reset.html', context)


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset link is invalid, please request a new one')
                return redirect('reset_password')

        except DjangoUnicodeDecodeError as identifier:
            messages.success(request, 'Invalid link')
            return render(request, 'authentication/password_change.html')
        return render(request, 'authentication/password_change.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset success, you can sign in with new password')
            return redirect('signin')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'authentication/password_change.html', context)

        return render(request, 'authentication/password_change.html', context)
