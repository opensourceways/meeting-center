#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 22:09
# @Author  : Tom_zc
# @FileName: meeting_group.py
# @Software: PyCharm

import logging

from meeting.infrastructure.dao.meeting_group_user_dao import MeetingGroupUserDao

logger = logging.getLogger("log")


class MeetingGroupApp:
    meeting_group_user_dao = MeetingGroupUserDao

    def get_groups(self, username):
        group_infos = list()
        group_users = self.meeting_group_user_dao.get_groups_by_username(username)
        for group_user in group_users:
            group_infos.append(group_user.group.to_dict())
        return group_infos
