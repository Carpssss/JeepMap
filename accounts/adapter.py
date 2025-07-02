from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponse
from allauth.account.adapter import DefaultAccountAdapter

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if not request.user.is_authenticated:
            raise ImmediateHttpResponse(HttpResponse(
                "Your Google account is not linked with any account in our system."
            ))
        return False