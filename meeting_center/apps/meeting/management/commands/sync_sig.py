#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/21 19:36
# @Author  : Tom_zc
# @FileName: sync_sig.py
# @Software: PyCharm

import logging

from django.conf import settings
from django.core.management import BaseCommand

from meeting_center.utils.request_handler import RequestHandler
from meeting.models import GroupInfo, GroupUser

logger = logging.getLogger("log")


class UserGroupDao:
    def __init__(self):
        self._group_dao = GroupInfo
        self._group_user_dao = GroupUser

    def save_to_db(self, sig_infos):
        group_names = self._group_dao.objects.all().distinct().values_list("group_name")
        exist_names = [group_name[0] for group_name in group_names]
        query_names = list(sig_infos.keys())
        need_delete_names = list(set(exist_names) - set(query_names))
        for group_name in sig_infos.keys():
            # 1.create group
            group = self._group_dao.objects.filter(group_name=group_name).first()
            if not group:
                group = self._group_dao.objects.create(
                    email_list=sig_infos[group_name]["email_list"],
                    group_name=sig_infos[group_name]["group_name"],
                    etherpad=sig_infos[group_name]["etherpad"],
                )
            else:
                self._group_dao.objects.filter(group_name=sig_infos[group_name]["group_name"]).update(
                    email_list=sig_infos[group_name]["email_list"],
                    etherpad=sig_infos[group_name]["etherpad"],
                )

            # 2.delete users
            user_names = self._group_user_dao.objects.filter(group__group_name=group_name) \
                .distinct().values("username")
            user_names = [user_name for user_name in user_names]
            need_delete = list(set(user_names) - set(sig_infos[group_name]["users"]))
            self._group_user_dao.objects.filter(username__in=need_delete).delete()
            # 3.add users
            for username in sig_infos[group_name]["users"]:
                count = self._group_user_dao.objects.filter(group=group, username=username).count()
                if count == 0:
                    self._group_user_dao.objects.create(group=group, username=username)
        # 3.delete group
        self._group_user_dao.objects.filter(group__group_name__in=need_delete_names).delete()
        self._group_dao.objects.filter(group_name__in=need_delete_names).delete()


class DsApi:
    def __init__(self):
        self._url = settings.DSAPI_URL
        self._request_handler = RequestHandler()
        self._dao = GroupInfo

    def _parse_data(self, sig_list):
        sig_infos = dict()
        for sig in sig_list:
            users = list()
            users.extend(sig["maintainers"])
            users.extend(sig["committers"])
            sig_info = {
                "email_list": sig["mailing_list"],
                "group_name": sig["sig_name"],
                "etherpad": "{}/p/{}".format(settings.COMMUNITY_ETHERPAD, sig["sig_name"]),
                "users": users
            }
            sig_infos.update({sig["sig_name"]: sig_info})
        return sig_infos

    def get_sig_info(self):
        _, resp_json = self._request_handler.get(self._url, is_suppress_error=False)
        return self._parse_data(resp_json["data"])


class Command(BaseCommand):
    def handle(self, *args, **options):
        ds_api = DsApi()
        data = ds_api.get_sig_info()
        user_group_dao = UserGroupDao()
        user_group_dao.save_to_db(data)
