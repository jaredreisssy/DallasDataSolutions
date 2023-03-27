from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from google.oauth2 import id_token
from google.auth.transport import requests
import google.auth

def landing_page(request):
    return render(request, 'landing_page.html')

def google_login(request):
    if request.method == 'POST':
        id_token_value = request.POST.get('id_token')
        try:
            # Verify the ID token using the Google Auth Library
            audience = 'your-google-client-id'
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
    return render(request, 'contact_us.html')
