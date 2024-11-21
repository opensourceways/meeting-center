#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 11:03
# @Author  : Tom_zc
# @FileName: my_permission.py
# @Software: PyCharm

import logging
from django.contrib.auth import get_user_model

from rest_framework import permissions

User = get_user_model()
logger = logging.getLogger('log')


class MaintainerCommitterPermission(permissions.IsAuthenticated):
    """Maintainer权限"""
    message = '需要Maintainer/Committer权限！！！'
    level = 2

    def has_permission(self, request, view):  # 对于列表的访问权限
        logger.info("check permission")
        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
