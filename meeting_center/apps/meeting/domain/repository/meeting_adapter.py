#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 15:39
# @Author  : Tom_zc
# @FileName: meeting_adapter.py
# @Software: PyCharm

from abc import ABC, abstractmethod


class MeetingAdapter(ABC):
    meeting_type = None

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_meeting_platform(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_meeting_date(self, *args, **kwargs):
        raise NotImplementedError