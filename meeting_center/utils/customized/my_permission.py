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

    def has_permission(self, request, view):
        from meeting.infrastructure.dao.meeting_group_user_dao import MeetingGroupUserDao
        users = MeetingGroupUserDao.get_groups_by_username(request.user.username)
        if len(users) == 0:
            logger.error("user:{} has no permission".format(request.user.username))
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
