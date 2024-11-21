#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 11:16
# @Author  : Tom_zc
# @FileName: models.py.py
# @Software: PyCharm
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """user model"""

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
