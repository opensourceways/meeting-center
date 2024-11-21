#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 10:57
# @Author  : Tom_zc
# @FileName: my_auth.py
# @Software: PyCharm
import logging
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.authentication import RemoteUserAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from meeting_center.utils.request_handler import RequestHandler

logger = logging.getLogger("log")

User = get_user_model()

_COOKIES_KEY = "authentication_key"
U_T = "_U_T_"
Y_G = "_Y_G_"


class AuthenticationAdapter(ABC):

    @abstractmethod
    def check(self, *args, **kwargs):
        raise NotImplementedError


class AuthenticationAdapterImpl(AuthenticationAdapter):

    def __init__(self):
        self._request_handler = RequestHandler()
        self._url = settings.ONEID_AUTHORIZATION_URL

    def check(self, cookies, headers):
        parse_headers = {
            "Token": cookies.get(U_T),
            "Referer": headers.get("Referer")
        }
        status_code, resp = self._request_handler.get(self._url, cookies=cookies, headers=parse_headers,
                                                      is_json=False, is_resp=True)
        if status_code != 200:
            logger.error("check authentication:{}, and return {}".format(str(status_code), resp))
            raise AuthenticationFailed('authentication failed', code='authentication_failed')
        json_data = resp.json()
        logger.info("receive the cookies:{}".format(resp.cookies))
        return json_data["data"], resp.cookies


def set_cookies_thread_local(request, value, key=_COOKIES_KEY):
    setattr(request, key, value)


def get_cookies_thread_local(request, key=_COOKIES_KEY):
    if hasattr(request, key):
        return getattr(request, key)
    return None


class CommunityAuthentication(RemoteUserAuthentication):
    def authenticate(self, request):
        authentication_adapter = AuthenticationAdapterImpl()
        user_info, cookies = authentication_adapter.check(request.COOKIES, request.META)
        set_cookies_thread_local(request, cookies)
        user = User(username=user_info["username"], is_active=True)
        return user, None
