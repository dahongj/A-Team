from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from .models import AllowlistURL


class LockedBrowserMiddleware(MiddlewareMixin):
    allowed_hosts = ['https://www.w3schools.com/python/']
    forbidden_hosts= ['https://www.youtube.com']

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # if 'is_in_lockdown' in request.session:
        #     allowed_urls  = [url.url for url in AllowlistURL.objects.filter(user=request.user)]
        #     if request.path not in allowed_urls:
        #         return HttpResponseForbidden("Access to this page is restricted during Focus Mode.")
        return self.get_response(request)
    
