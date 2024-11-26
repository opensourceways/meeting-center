#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 20:41
# @Author  : TomNewChao
# @File    : request_handler.py
# @Description :
import requests
from requests.auth import HTTPBasicAuth
# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestHandler:
    def __init__(self, username=None, password=None, timeout=None, verify=True):
        self.timeout = timeout if not timeout else 60
        if username and password:
            self._auth = HTTPBasicAuth(username, password)
        else:
            self._auth = None
        self.verify = verify

    def get(self, url, cookies=None, headers=None, is_json=True, is_resp=False, is_suppress_error=True):
        resp = requests.get(url, auth=self._auth, cookies=cookies, headers=headers,
                            timeout=(self.timeout, self.timeout), verify=self.verify)
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "get the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        if is_json:
            return resp.status_code, resp.json()
        if is_resp:
            return resp.status_code, resp
        return resp.status_code, resp.content

    def post(self, url, json_data=None, data=None, is_suppress_error=True):
        resp = requests.post(url, auth=self._auth, json=json_data, data=data,
                             timeout=(self.timeout, self.timeout), verify=self.verify)
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "post the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()

    def put(self, url, json_data=None, data=None, is_suppress_error=True):
        resp = requests.put(url, auth=self._auth, json=json_data, data=data,
                            timeout=(self.timeout, self.timeout), verify=self.verify)
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "put the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()

    def delete(self, url, is_suppress_error=True):
        resp = requests.delete(url, auth=self._auth, timeout=(self.timeout, self.timeout), verify=self.verify)
        if not str(resp.status_code).startswith("20") and not is_suppress_error:
            raise RuntimeError(
                "delete the url failed, return status is:{} the detail is:{}".format(resp.status_code, resp.content))
        return resp.status_code, resp.json()
