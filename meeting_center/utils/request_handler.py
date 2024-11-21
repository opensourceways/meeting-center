#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 20:41
# @Author  : TomNewChao
# @File    : request_handler.py
# @Description :
import requests
from requests.auth import HTTPBasicAuth


class RequestHandler:
    def __init__(self, username, password, timeout=None):
        self.timeout = timeout if not timeout else 60
        self._auth = HTTPBasicAuth(username, password)

    def get(self, url, is_json=True, is_suppress_error=True):
        resp = requests.get(url, auth=self._auth, timeout=(self.timeout, self.timeout))
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "get the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        if is_json:
            return resp.status_code, resp.json()
        return resp.status_code, resp.content

    def post(self, url, json_data=None, data=None, is_suppress_error=True):
        resp = requests.post(url, auth=self._auth, json=json_data, data=data, timeout=(self.timeout, self.timeout))
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "post the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()

    def put(self, url, json_data=None, data=None, is_suppress_error=True):
        resp = requests.put(url, auth=self._auth, json=json_data, data=data, timeout=(self.timeout, self.timeout))
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "put the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()

    def delete(self, url, is_suppress_error=True):
        resp = requests.delete(url, auth=self._auth, timeout=(self.timeout, self.timeout))
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "delete the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()
