from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from transformers import pipeline
from django.core.mail import send_mail
from django.conf import settings


import google.auth

from base_app.oai_queries import get_completion


def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    return render(request, 'query.html')

def landing_page(request):
    return render(request, 'landing_page.html')


def google_login(request):
    if request.method == 'POST':
        id_token_value = request.POST.get('id_token')
        try:
            idinfo = id_token.verify_oauth2_token(id_token_value, requests.Request(), settings.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            user_email = idinfo['email']
            user = authenticate(request, username=user_email, password=None)
            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                return redirect('landing_page')
        except ValueError:
            return redirect('landing_page')
    else:
        return redirect('landing_page')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            'New message from Contact Us form',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,
            ['your_email_address'],
            fail_silently=False,
        )
        return redirect('success')
    else:
        return render(request, 'contact_us.html')


