# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 18:44
# @Author  : Tom_zc
# @FileName: my_serializers.py
# @Software: PyCharm


class MyBaseSerializer:
    def validate(self, kwargs):
        new_dict = dict()
        for field, value in kwargs.items():
            check_param_func_name = "validate_{}".format(field)
            if hasattr(self, check_param_func_name):
                fun = getattr(self, check_param_func_name)
                new_dict[field] = fun(value)
        return new_dict
