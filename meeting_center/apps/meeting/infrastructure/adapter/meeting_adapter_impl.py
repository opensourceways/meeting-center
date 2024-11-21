#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:18
# @Author  : Tom_zc
# @FileName: bilibili_client.py
# @Software: PyCharm
from django.conf import settings
from urllib.parse import urlencode

from meeting.domain.repository.meeting_adapter import MeetingAdapter
from meeting_center.utils.request_handler import RequestHandler


class MeetingAdapterImpl(MeetingAdapter):
    create_url = "{}/inner/v1/meeting/meeting/"
    list_url = "{}/inner/v1/meeting/meeting/?{}"
    get_url = "{}/inner/v1/meeting/meeting/{}/"
    put_url = "{}/inner/v1/meeting/meeting/{}/"
    delete_url = "{}/inner/v1/meeting/meeting/{}/"
    get_meeting_platform_url = "{}/inner/v1/meeting/meeting/platform/?{}"
    get_meeting_date_url = "{}/inner/v1/meeting/meeting/date/?{}"
    get_meeting_by_date_url = "{}/inner/v1/meeting/meeting/?{}"

    def __init__(self, meeting_platform_info=settings.MEETING_PLATFORM):
        """init meeting adapter impl"""
        self.url = meeting_platform_info.get("URL")
        username = meeting_platform_info.get("USERNAME")
        pwd = meeting_platform_info.get("PASSWORD")
        self._request_handler = RequestHandler(username, pwd)

    def create(self, meeting_data):
        url = self.create_url.format(self.url)
        return self._request_handler.post(url, json_data=meeting_data)

    def update(self, meeting_id, meeting_data):
        url = self.put_url.format(self.url, meeting_id)
        return self._request_handler.put(url, json_data=meeting_data)

    def delete(self, meeting_id, **kwargs):
        url = self.delete_url.format(self.url, meeting_id)
        return self._request_handler.delete(url)

    def get(self, meeting_id, **kwargs):
        url = self.get_url.format(self.url, meeting_id)
        return self._request_handler.get(url)

    def list(self, **kwargs):
        query_string = urlencode(kwargs)
        url = self.list_url.format(self.url, query_string)
        return self._request_handler.get(url)

    def get_meeting_platform(self, **kwargs):
        query_string = urlencode(kwargs)
        url = self.get_meeting_platform_url.format(self.url, query_string)
        return self._request_handler.get(url)

    def get_meeting_date(self, **kwargs):
        query_string = urlencode(kwargs)
        url = self.get_meeting_date_url.format(self.url, query_string)
        return self._request_handler.get(url)
