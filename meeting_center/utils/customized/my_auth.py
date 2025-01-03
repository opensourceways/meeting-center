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
        token = headers.get("HTTP_TOKEN") or headers.get("Token")
        if token != cookies.get(U_T):
            logger.error("check authentication failed and token is not consistency")
            raise AuthenticationFailed('authentication failed', code='authentication_failed')
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
        identities = json_data["data"].get("identities")
        if isinstance(identities, list):
            login_names = [identity["login_name"] for identity in identities if identity["identity"] == "gitcode"]
            if len(login_names) > 0:
                return login_names[0], resp.cookies
        logger.error("check authentication invalid identities")
        raise AuthenticationFailed('authentication failed', code='authentication_failed')


def set_cookies_thread_local(request, value, key=_COOKIES_KEY):
    setattr(request, key, value)


def get_cookies_thread_local(request, key=_COOKIES_KEY):
    if hasattr(request, key):
        return getattr(request, key)
    return None


class CommunityAuthentication(RemoteUserAuthentication):
    def authenticate(self, request):
        authentication_adapter = AuthenticationAdapterImpl()
        username, cookies = authentication_adapter.check(request.COOKIES, request.META)
        set_cookies_thread_local(request, cookies)
        user = User(username=username, is_active=True)
        return user, None
