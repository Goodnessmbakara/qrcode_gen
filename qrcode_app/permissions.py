# permissions.py
from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import IPAddressAPIKey

class HasIPAddressAPIKey(BaseHasAPIKey):
    model = IPAddressAPIKey

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)

        if has_permission:
            key = request.META["HTTP_AUTHORIZATION"].split()[0]
            api_key = IPAddressAPIKey.objects.get_from_key(key)
            ip_address = request.META.get('REMOTE_ADDR') # Get the IP address of the request

            return api_key.ip_address == ip_address

        return False
