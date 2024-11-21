#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 21:57
# @Author  : Tom_zc
# @FileName: meeting_group_user_dao.py.py
# @Software: PyCharm

from meeting.models import GroupUser


class MeetingGroupUserDao:
    dao = GroupUser

    @classmethod
    def get_groups_by_username(cls, username):
        return cls.dao.objects.filter(username=username).all()



