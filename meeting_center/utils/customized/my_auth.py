#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 10:57
# @Author  : Tom_zc
# @FileName: my_auth.py
# @Software: PyCharm
from django.contrib.auth import get_user_model
from rest_framework.authentication import RemoteUserAuthentication

User = get_user_model()


class CommunityAuthentication(RemoteUserAuthentication):
    def authenticate(self, request):
        """todo something"""
        user = User.objects.first()
        return user, None
