#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 17:08
# @Author  : Tom_zc
# @FileName: meeting_serializers.py
# @Software: PyCharm

import logging
from datetime import datetime

from django.conf import settings

from meeting_center.utils.check_params import check_field, check_invalid_content, check_email_list, check_date, \
    check_time, check_link, check_duration
from meeting_center.utils.customized.my_serializers import MyBaseSerializer
from meeting_center.utils.ret_api import MyValidationError
from meeting_center.utils.ret_code import RetCode

logger = logging.getLogger("log")


class MeetingSerializer(MyBaseSerializer):
    """MeetingSerializer for get a meeting and create meeting"""

    def validate_sponsor(self, value):
        """check length of 64"""
        check_field(value, 64)
        check_invalid_content(value)
        return value

    def validate_group_name(self, value):
        """check length of 64"""
        check_field(value, 64)
        check_invalid_content(value)
        return value

    def validate_community(self, value):
        """check community"""
        if value not in settings.COMMUNITY_SUPPORT:
            logger.error("community {} is not exist in COMMUNITY_SUPPORT".format(value))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        return value

    def validate_topic(self, value):
        """check length of 128，not include \r\n url xss"""
        check_field(value, 128)
        check_invalid_content(value)
        return value

    def validate_platform(self, value):
        """check platform"""
        return value

    def validate_date(self, value):
        """check date"""
        check_date(value)
        return value

    def validate_start(self, value):
        """check start"""
        check_time(value)
        return value

    def validate_end(self, value):
        """check end"""
        check_time(value)
        return value

    def validate_is_record(self, value):
        """check record"""
        if not isinstance(value, bool):
            logger.error("invalid is_record:{}".format(value))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        return value

    def validate_etherpad(self, value):
        """check etherpad"""
        if value:
            check_link(value)
            return value

    def validate_agenda(self, value):
        """check agenda"""
        if value:
            check_field(value, 4096)
            check_invalid_content(value, check_crlf=False)
            return value

    def validate_email_list(self, value):
        """check email_list"""
        if value:
            check_email_list(value)
            return value

    def validate(self, attrs):
        super(MeetingSerializer, self).__init__(attrs)
        etherpad = attrs.get("etherpad")
        if etherpad is not None and not etherpad.startswith(settings.COMMUNITY_ETHERPAD[attrs["community"]]):
            logger.error("invalid etherpad:{}".format(etherpad))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        check_duration(attrs["start"], attrs["end"], attrs["date"], datetime.now())
        if attrs["platform"] not in settings.COMMUNITY_HOST[attrs["community"]].keys():
            logger.error('platform {} is not exist in COMMUNITY_HOST.'.format(attrs["platform"]))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        return attrs


class SingleMeetingSerializer(MeetingSerializer):
    """UpdateMeetingSerializer for update meeting"""

    def validate_topic(self, value):
        """check length of 128，not include \r\n url xss"""
        check_field(value, 128)
        check_invalid_content(value)
        return value

    def validate_date(self, value):
        """check date"""
        check_date(value)
        return value

    def validate_start(self, value):
        """check start"""
        check_time(value)
        return value

    def validate_end(self, value):
        """check end"""
        check_time(value)
        return value

    def validate_agenda(self, value):
        """check agenda"""
        if value:
            check_field(value, 4096)
            check_invalid_content(value, check_crlf=False)
            return value

    def validate_etherpad(self, value):
        """check etherpad"""
        if value:
            check_link(value)
            return value

    def validate_is_record(self, value):
        """check record"""
        if not isinstance(value, bool):
            logger.error("invalid is_record:{}".format(value))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        return value

    def validate(self, attrs):
        """all validate data"""
        super(SingleMeetingSerializer, self).__init__(attrs)
        check_duration(attrs["start"], attrs["end"], attrs["date"], datetime.now())
        attrs["update_time"] = datetime.now()
        return attrs
