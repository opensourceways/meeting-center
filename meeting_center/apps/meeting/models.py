#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 11:16
# @Author  : Tom_zc
# @FileName: models.py.py
# @Software: PyCharm
from itertools import chain

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """user model"""

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class GroupInfo(models.Model):
    """SIG组"""
    group_name = models.CharField(verbose_name='SIG组名', max_length=128, unique=True)
    email_list = models.EmailField(verbose_name='邮件列表', null=True, blank=True)
    etherpad = models.CharField(verbose_name='etherpad', max_length=255, null=True, blank=True)

    class Meta:
        db_table = "meeting_group"
        verbose_name = "meeting_group"
        verbose_name_plural = verbose_name

    # noinspection PyUnresolvedReferences
    def to_dict(self, fields=None, exclude=None, is_relate=False):
        """to dict"""
        dict_data = dict()
        for f in chain(self._meta.concrete_fields, self._meta.many_to_many):
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, models.ManyToManyField):
                if is_relate is False:
                    continue
                value = [i.to_dict() for i in value] if self.pk else None
            if isinstance(f, models.DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            dict_data[f.name] = value
        return dict_data


class GroupUser(models.Model):
    """SIG组与用户表"""
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE)
    username = models.CharField(verbose_name='maintainer/committer', max_length=64)

    class Meta:
        db_table = "meeting_group_user"
        verbose_name = "meeting_group_user"
        verbose_name_plural = verbose_name
