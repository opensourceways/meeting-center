#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 11:22
# @Author  : Tom_zc
# @FileName: meeting_controller.py
# @Software: PyCharm


from django.urls import path

from meeting.controller.meeting_controller import MeetingView, SingleMeetingView, \
    MeetingParticipantsView, MeetingPlatformView

urlpatterns = [
    path('meeting/', MeetingView.as_view()),  # 预定会议/会议列表
    path('meeting/<int:id>/', SingleMeetingView.as_view()),  # 修改/删除/查询单个会议
    path('meeting/participants/<int:id>/', MeetingParticipantsView.as_view()),  # 查询会议参与人
    path('meeting/platform/', MeetingPlatformView.as_view())  # 获取会议类型
]
