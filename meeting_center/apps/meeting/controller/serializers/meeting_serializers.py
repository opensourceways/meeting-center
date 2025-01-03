#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 17:08
# @Author  : Tom_zc
# @FileName: meeting_serializers.py
# @Software: PyCharm

import logging
import traceback
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
    write_fields = [
        "topic", "group_name", "platform", "date", "start", "end", "is_record"
    ]

    def validate_group_name(self, value):
        """check length of 64"""
        check_field(value, 64)
        check_invalid_content(value)
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
        value = check_date(value)
        return value.strftime('%Y-%m-%d')

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
        # check the required parameters
        lack_params = set(self.write_fields) - set(list(attrs.keys()))
        if lack_params:
            logger.error("create meeting lack the params:{}".format(lack_params))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        # check every params
        super(MeetingSerializer, self).validate(attrs)
        # check the etherpad
        etherpad = attrs.get("etherpad")
        if etherpad is not None and not etherpad.startswith(settings.COMMUNITY_ETHERPAD):
            logger.error("invalid etherpad:{}".format(etherpad))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        check_duration(attrs["start"], attrs["end"], attrs["date"], datetime.now())
        return attrs


class SingleMeetingSerializer(MyBaseSerializer):
    """UpdateMeetingSerializer for update meeting"""
    write_fields = [
        "topic", "date", "start", "end", "is_record"
    ]

    def validate_topic(self, value):
        """check length of 128，not include \r\n url xss"""
        check_field(value, 128)
        check_invalid_content(value)
        return value

    def validate_date(self, value):
        """check date"""
        value = check_date(value)
        return value.strftime('%Y-%m-%d')

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
        try:
            # 1.check requirements
            lack_params = set(self.write_fields) - set(list(attrs.keys()))
            if lack_params:
                logger.error("put meeting lack the params:{}".format(lack_params))
                raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
            # 2.check every params
            super(SingleMeetingSerializer, self).validate(attrs)
            # 3.check the etherpad
            etherpad = attrs.get("etherpad")
            if etherpad is not None and not etherpad.startswith(settings.COMMUNITY_ETHERPAD):
                logger.error("invalid etherpad:{}".format(etherpad))
                raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
            check_duration(attrs["start"], attrs["end"], attrs["date"], datetime.now())
            return attrs
        except (ValueError, KeyError) as e:
            logger.info("e:{}, traceback:{}".format(e, traceback.format_exc()))
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
