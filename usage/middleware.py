from .models import PageHit
from django.contrib.auth import get_user


class UsageMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            PageHit.objects.create(
                user=get_user(request),
                requested_page=request.path_info,
                user_agent=request.META['HTTP_USER_AGENT'])
        else:
            pass
