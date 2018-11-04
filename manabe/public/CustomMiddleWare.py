from django.middleware.clickjacking import XFrameOptionsMiddleware
from django.conf import settings


class TFXFrameOptionsMiddleware(XFrameOptionsMiddleware):
    def get_xframe_options_value(self, request, response):
        if request.META['REMOTE_ADDR'] in settings.XFRAME_EXEMPT_IPS:
            return 'ALLOW-FROM http://127.0.0.1:8888/'  # non standard, equivalent to omitting
        return getattr(settings, 'X_FRAME_OPTIONS', 'SAMEORIGIN').upper()