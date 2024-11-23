# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 15:22
# @Author  : Tom_zc
# @FileName: my_middleware.py
# @Software: PyCharm
import logging
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from urllib.parse import urlparse

logger = logging.getLogger("log")


class MyMiddleware(MiddlewareMixin):

    def _is_subdomain(self, parent_domain, referer_url):
        """judge the subdomain is sub domain of parent_domain"""
        if not referer_url:
            return False

        url_object = urlparse(referer_url)
        subdomain = url_object.netloc
        subdomain_parts = subdomain.split('.')

        parent_parts = parent_domain.split('.')

        if len(subdomain_parts) < len(parent_parts):
            return False

        return subdomain_parts[-2:] == parent_parts[-2:]

    def process_request(self, request):
        if isinstance(request, HttpRequest):
            if settings.REFERER_DOMAIN and not self._is_subdomain(settings.REFERER_DOMAIN,
                                                                  request.headers.get("Referer")):
                return HttpResponse(status=403, content="invalid referer")

    def process_response(self, _, response):
        if isinstance(response, HttpResponseBase):
            response["X-XSS-Protection"] = "1; mode=block"
            response["X-Frame-Options"] = "DENY"
            response["X-Content-Type-Options"] = "nosniff"
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response["Content-Security-Policy"] = "script-src 'self'; object-src 'none'; frame-src 'none'"
            response["Cache-Control"] = "no-cache,no-store,must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = 0
            response["Referrer-Policy"] = "no-referrer"
        return response
