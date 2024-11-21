#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 11:22
# @Author  : Tom_zc
# @FileName: meeting_controller.py
# @Software: PyCharm


from django.urls import path

from meeting.controller.meeting_controller import MeetingView, SingleMeetingView, MeetingPlatformView, \
    MeetingDateView, MeetingsView, MeetingGroupView

urlpatterns = [
    path('meeting/', MeetingView.as_view()),  # 预定会议/会议列表
    path('meeting/<int:id>/', SingleMeetingView.as_view()),  # 修改/删除/查询单个会议
    path('meeting/platform/', MeetingPlatformView.as_view()),  # 获取会议类型
    path('meeting/group_info/', MeetingGroupView.as_view()),  # 获取用户所属组的列表
    path('meeting/meeting_date/', MeetingDateView.as_view()),  # 获取会议时间（官网）
    path('meeting/meeting/', MeetingsView.as_view()),  # 获取会议数据（官网）
]
