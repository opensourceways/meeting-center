#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/25 17:58
# @Author  : Tom_zc
# @FileName: my_exception.py
# @Software: PyCharm

from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from meeting_center.utils.ret_code import RetCode


def my_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, AuthenticationFailed):
        msg = RetCode.get_name_by_code(RetCode.STATUS_AUTH_FAILED)
        resp_status = status.HTTP_401_UNAUTHORIZED
        data = {
            'msg': msg,
            'code': resp_status,
            'data': None
        }
        return Response(data, status=resp_status)

    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = {
            'msg': exc.detail,
            'code': exc.status_code,
            'data': None
        }

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
