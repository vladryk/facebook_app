import json
import base64
import hmac
import hashlib

from allauth.socialaccount.models import SocialAccount, SocialApp

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import get_user, logout


class HomePageView(TemplateView):
    template_name = "fb/home.html"


class DeauthView(View):
    def post(self, request, *args, **kwargs):
        try:
            secret = SocialApp.objects.get(name=getattr(settings, "SOCIAL_APP_NAME", None)).secret
        except SocialApp.DoesNotExist:
            return HttpResponse(status=404, content='Could not find SocialApp')

        try:
            signed_request = request.POST['signed_request']
            encoded_sig, payload = signed_request.split('.')
        except KeyError:
            return HttpResponse(status=400, content='Invalid request')

        # decode data
        try:
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode('utf-8')
            decoded_payload = json.loads(decoded_payload)

            sig = base64.urlsafe_b64decode(encoded_sig + "==")
            expected_sig = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256)
        except Exception:
            return HttpResponse(status=400, content='Could not decode payload or signature')

        # confirm the signature
        if not hmac.compare_digest(expected_sig.digest(), sig):
            return HttpResponse(status=400, content='Invalid request')

        user_id = decoded_payload['user_id']

        try:
            account = SocialAccount.objects.get(uid=user_id)
        except SocialAccount.DoesNotExist:
            return HttpResponse(status=200, content='Seems like this social account has already removed')

        logout(request)
        account.user.is_active = False
        account.user.save()

        return HttpResponse(status=200)
