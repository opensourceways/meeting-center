#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 14:11
# @Author  : Tom_zc
# @FileName: meeting_controller.py
# @Software: PyCharm
from rest_framework.generics import GenericAPIView

from meeting_center.utils.customized.my_auth import CommunityAuthentication
from meeting_center.utils.customized.my_permission import MaintainerCommitterPermission
from meeting_center.utils.ret_api import ret_json, capture_my_validation_exception, MyValidationError, MyNoPermission
from meeting_center.utils.operation_log import OperationLogModule, OperationLogDesc, OperationLogType, \
    logger_wrapper, set_log_thread_local, log_key

from meeting.application.meeting import MeetingApp
from meeting.controller.serializers.meeting_serializers import MeetingSerializer, \
    SingleMeetingSerializer
from meeting_center.utils.ret_code import RetCode


class MeetingView(GenericAPIView):
    """create or list meeting"""
    serializer_class = MeetingSerializer()
    authentication_classes = (CommunityAuthentication,)
    permission_classes = (MaintainerCommitterPermission,)
    app_class = MeetingApp()
    order_by = ["date", "create_time", "update_time"]
    order_type = ["asc", "desc"]

    @capture_my_validation_exception
    @logger_wrapper(OperationLogModule.OP_MODULE_MEETING, OperationLogType.OP_TYPE_CREATE,
                    OperationLogDesc.OP_DESC_MEETING_CREATE_CODE)
    def post(self, request, *args, **kwargs):
        """create meeting api"""
        set_log_thread_local(request, log_key, [request.data.get('topic')])
        meeting = self.serializer_class.validate(request.data)
        status_code, data = self.app_class.create(request, meeting)
        return ret_json(status_code=status_code, **data)

    def get(self, request, *args, **kwargs):
        """list the meeting"""
        page = self.request.query_params.get("page")
        size = self.request.query_params.get("size")
        order_by = request.query_params.get("order_by")
        if order_by and order_by not in self.order_by:
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        if not order_by:
            order_by = "date"
        order_type = self.request.query_params.get("order_type")
        if order_type and order_type not in self.order_type:
            raise MyValidationError(RetCode.STATUS_PARAMETER_ERROR)
        status_code, data = self.app_class.list(request.user.username, page, size,
                                                order_by, order_type)
        return ret_json(status_code=status_code, **data)


class SingleMeetingView(GenericAPIView):
    """get or update or delete meeting"""
    serializer_class = SingleMeetingSerializer()
    authentication_classes = (CommunityAuthentication,)
    permission_classes = (MaintainerCommitterPermission,)
    app_class = MeetingApp()

    def get(self, request, *args, **kwargs):
        """get meeting api"""
        meeting_id = kwargs.get('id')
        status_code, data = self.app_class.get(meeting_id=meeting_id)
        return ret_json(status_code=status_code, **data)

    @capture_my_validation_exception
    @logger_wrapper(OperationLogModule.OP_MODULE_MEETING, OperationLogType.OP_TYPE_MODIFY,
                    OperationLogDesc.OP_DESC_MEETING_UPDATE_CODE)
    def put(self, request, *args, **kwargs):
        """update meeting api"""
        set_log_thread_local(request, log_key, ['', kwargs.get('id')])
        meeting_id = kwargs.get('id')
        status_code, data = self.app_class.get(meeting_id=meeting_id)
        if status_code != 200 or data["code"] != 200:
            return ret_json(status_code=status_code, **data)
        if data["data"]["sponsor"] != request.user.username:
            raise MyNoPermission(RetCode.STATUS_MEETING_NO_PERMISSION)
        set_log_thread_local(request, log_key, [data["data"]["topic"], kwargs.get('id')])
        meeting = self.serializer_class.validate(request.data)
        status_code, data = self.app_class.update(meeting_id, meeting)
        return ret_json(status_code=status_code, **data)

    @capture_my_validation_exception
    @logger_wrapper(OperationLogModule.OP_MODULE_MEETING, OperationLogType.OP_TYPE_DELETE,
                    OperationLogDesc.OP_DESC_MEETING_DELETE_CODE)
    def delete(self, request, *args, **kwargs):
        """delete meeting by mid"""
        set_log_thread_local(request, log_key, ['', kwargs.get('id')])
        meeting_id = kwargs.get('id')
        status_code, data = self.app_class.get(meeting_id=meeting_id)
        if status_code != 200 or data["code"] != 200:
            return ret_json(status_code=status_code, **data)
        if data["data"]["sponsor"] != request.user.username:
            raise MyNoPermission(RetCode.STATUS_MEETING_NO_PERMISSION)
        set_log_thread_local(request, log_key, [data["data"]["topic"], kwargs.get('id')])
        status_code, data = self.app_class.delete(meeting_id)
        return ret_json(status_code=status_code, **data)


class MeetingPlatformView(GenericAPIView):
    authentication_classes = (CommunityAuthentication,)
    permission_classes = (MaintainerCommitterPermission,)
    app_class = MeetingApp()

    def get(self, request, *args, **kwargs):
        """get meeting platform"""
        status_code, data = self.app_class.get_meeting_platform()
        return ret_json(status_code=status_code, **data)


class MeetingDateView(GenericAPIView):
    app_class = MeetingApp()

    def get(self, request, *args, **kwargs):
        """get meeting date in website"""
        date = self.request.query_params.get("date")
        status_code, data = self.app_class.get_meeting_date(date)
        return ret_json(status_code=status_code, **data)


class MeetingsView(GenericAPIView):
    app_class = MeetingApp()

    def get(self, request, *args, **kwargs):
        """get meeting date in website"""
        date = self.request.query_params.get("date")
        status_code, data = self.app_class.get_meeting_data(date)
        return ret_json(status_code=status_code, **data)
