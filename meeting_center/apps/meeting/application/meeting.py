#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 14:59
# @Author  : Tom_zc
# @FileName: meeting.py
# @Software: PyCharm
import logging

from meeting.infrastructure.adapter.meeting_adapter_impl import MeetingAdapterImpl

logger = logging.getLogger("log")


class MeetingApp:
    meeting_adapter_impl = MeetingAdapterImpl()

    def create(self, meeting):
        """create meeting"""
        return self.meeting_adapter_impl.create(meeting)

    def update(self, meeting_id, meeting_data):
        """update meeting"""
        return self.meeting_adapter_impl.update(meeting_id, **meeting_data)

    def delete(self, meeting_id):
        """delete meeting"""
        return self.meeting_adapter_impl.delete(meeting_id)

    def get(self, meeting_id):
        return self.meeting_adapter_impl.get(meeting_id=meeting_id)

    def list(self):
        return self.meeting_adapter_impl.list()

    def get_meeting_platform(self):
        """get platform"""
        return self.meeting_adapter_impl.get_meeting_platform()
