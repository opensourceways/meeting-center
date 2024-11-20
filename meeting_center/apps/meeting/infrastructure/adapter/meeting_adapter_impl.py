#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:18
# @Author  : Tom_zc
# @FileName: bilibili_client.py
# @Software: PyCharm
from django.conf import settings

from meeting.domain.repository.meeting_adapter import MeetingAdapter
from meeting_center.utils.request_handler import RequestHandler


class MeetingAdapterImpl(MeetingAdapter):
    create_url = "/inner/v1/meeting/meeting/"
    list_url = "/inner/v1/meeting/meeting/"
    get_url = "/inner/v1/meeting/meeting/{}/"
    put_url = "/inner/v1/meeting/meeting/{}/"
    delete_url = "/inner/v1/meeting/meeting/{}/"
    get_meeting_platform_url = "/inner/v1/meeting/platform/"

    def __init__(self, reqeust_handler=RequestHandler()):
        """init meeting adapter impl"""
        self._request_handler = reqeust_handler

    def create(self, *args, **kwargs):
        return self._request_handler.post(self.create_url, json_data=kwargs)

    def update(self, meeting_id, **kwargs):
        url = self.put_url.format(meeting_id)
        return self._request_handler.put(url, json_data=kwargs)

    def delete(self, meeting_id, **kwargs):
        url = self.delete_url.format(meeting_id)
        return self._request_handler.delete(url)

    def get(self, meeting_id, **kwargs):
        url = self.get_url.format(meeting_id)
        return self._request_handler.get(url)

    def list(self, *args, **kwargs):
        return self._request_handler.get(self.list_url)

    def get_meeting_platform(self, *args, **kwargs):
        return self._request_handler.get(self.get_meeting_platform_url)

    def get_meeting_date(self, *args, **kwargs):
        pass

    def get_meeting_by_date(self, *args, **kwargs):
        pass
