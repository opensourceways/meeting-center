#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 19:43
# @Author  : Tom_zc
# @FileName: my_view.py
# @Software: PyCharm
from rest_framework.generics import GenericAPIView

from meeting_center.utils.ret_api import ret_json


class PingView(GenericAPIView):
    """get the heartbeat"""

    def retrieve(self, request, *args, **kwargs):
        """get the status of service"""
        return ret_json(msg='the status is ok')
