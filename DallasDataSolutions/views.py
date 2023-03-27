from django.shortcuts import render
import google.auth
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import redirect

def landing_page(request):
    return render(request, 'landing_page.html')


def google_login(request):
    if request.method == 'POST':
        id_token = request.POST.get('id_token')
        try:
            # Verify the ID token using the Google Auth Library
            audience = 'your-google-client-id'
            id_info = id_token.verify_oauth2_token(id_token, requests.Request(), audience)

            # If the ID token is valid, log the user in
            user = authenticate(request, google_id=id_info['sub'])
            login(request, user)

            return redirect('home')
        except ValueError:
            # Invalid token
            pass

    return render(request, 'google_login.html')