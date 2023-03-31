from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from transformers import pipeline
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


import google.auth

def landing_page(request):
    return render(request, 'landing_page.html')

def google_login(request):
    if request.method == 'POST':
        id_token_value = request.POST.get('id_token')
        try:
            # Verify the ID token using the Google Auth Library
            audience = 'MTG'
            id_info = id_token.verify_oauth2_token(id_token_value, requests.Request(), audience)

            # If the ID token is valid, log the user in
            user = authenticate(request, google_id=id_info['sub'])
            login(request, user)

            return redirect('home')
        except ValueError:
            # Invalid token
            pass

    return render(request, 'google_login.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = 'Message from your website'
        from_email = email
        to_email = [settings.EMAIL_HOST_USER]
        body = f"Name: {name}\n\nEmail: {email}\n\nMessage: {message}"
        send_mail(subject, body, from_email, to_email, fail_silently=False)

        # Render success message
        return render(request, 'success.html')

    # Render the contact form
    return render(request, 'contact_us.html')
def chat_bot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # initialize the chatgpt pipeline
        chatbot = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
        # generate the chat bot response
        chatbot_response = chatbot(user_input, max_length=50, do_sample=True, temperature=0.7)[0]['generated_text']
        return render(request, 'chat_bot.html', {'user_input': user_input, 'chatbot_response': chatbot_response})
    else:
        return render(request, 'chat_bot.html')