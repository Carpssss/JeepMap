from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model

class NoNewUsersSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Only allow login if user already exists
        email = sociallogin.user.email
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            messages.error(request, "This Google account is not registered. Please sign up first.")
            raise ImmediateHttpResponse(redirect(reverse('login')))