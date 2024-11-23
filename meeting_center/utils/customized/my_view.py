#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 19:43
# @Author  : Tom_zc
# @FileName: my_view.py
# @Software: PyCharm
from rest_framework.generics import GenericAPIView

from meeting_center.utils.customized.my_auth import get_cookies_thread_local, U_T, Y_G
from meeting_center.utils.ret_api import ret_json


class PingView(GenericAPIView):
    """get the heartbeat"""

    def retrieve(self, request, *args, **kwargs):
        """get the status of service"""
        return ret_json(msg='the status is ok')


class MyGenericAPIView(GenericAPIView):
    """my generic API view"""

    # noinspection PyAttributeOutsideInit
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        cookies = get_cookies_thread_local(request)
        if cookies:
            for cookie in cookies:
                if cookie.name not in [U_T, Y_G]:
                    continue
                cookie_data = dict(value=cookie.value,
                                   expires=1800,
                                   path="/",
                                   domain=cookie.domain,
                                   secure=True)
                if cookie.name == Y_G:
                    cookie_data["httponly"] = True
                self.response.set_cookie(cookie.name, **cookie_data)
        return self.response
