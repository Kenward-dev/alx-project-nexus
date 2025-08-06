from datetime import datetime
from django.conf import settings

def site_info(request):
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'Polls API'),
        'domain': request.get_host() if request else 'localhost:8000',
        'now': datetime.now(),
    }