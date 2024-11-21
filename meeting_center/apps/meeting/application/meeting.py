#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 14:59
# @Author  : Tom_zc
# @FileName: meeting.py
# @Software: PyCharm
import logging
from django.conf import settings

from meeting.infrastructure.adapter.meeting_adapter_impl import MeetingAdapterImpl

logger = logging.getLogger("log")


class MeetingApp:
    meeting_adapter_impl = MeetingAdapterImpl()

    def create(self, request, meeting_data):
        """create meeting"""
        meeting_data["community"] = settings.COMMUNITY
        meeting_data["sponsor"] = request.user.username
        return self.meeting_adapter_impl.create(meeting_data)

    def update(self, meeting_id, meeting_data):
        """update meeting"""
        return self.meeting_adapter_impl.update(meeting_id, meeting_data)

    def delete(self, meeting_id):
        """delete meeting"""
        return self.meeting_adapter_impl.delete(meeting_id)

    def get(self, meeting_id):
        """get single meeting"""
        return self.meeting_adapter_impl.get(meeting_id=meeting_id)

    def list(self, sponsor, page, size, order_by, order_type):
        """list meeting"""
        query_condition = {
            "sponsor": sponsor,
            "community": settings.COMMUNITY
        }
        if order_by:
            query_condition["order_by"] = order_by
        if order_type:
            query_condition["order_type"] = order_type
        if page:
            query_condition["page"] = page
        if size:
            query_condition["size"] = size
        return self.meeting_adapter_impl.list(**query_condition)

    def get_meeting_platform(self):
        """get meeting platform"""
        query_condition = {
            "community": settings.COMMUNITY
        }
        return self.meeting_adapter_impl.get_meeting_platform(**query_condition)

    def get_meeting_date(self, date):
        """get meeting date"""
        query_condition = {
            "community": settings.COMMUNITY,
        }
        if date:
            query_condition["date"] = date
        return self.meeting_adapter_impl.get_meeting_date(**query_condition)

    def get_meeting_data(self, date):
        """get meeting date"""
        query_condition = {
            "community": settings.COMMUNITY,
            "date": date,
            "is_delete": False
        }
        return self.meeting_adapter_impl.list(**query_condition)
