#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from spider163 import settings
from spider163.spider import public as uapi
from spider163.spider.common import encSecKey, create_params_by_dict
from spider163.utils import pylog
from spider163.utils import tools

r_1080p = 1808
r_720p = 720
r_480p = 480
r_240p = 240
default_r = r_720p


class MV:
    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()
        self.__encSecKey = encSecKey
        self.default_r = 720

    def get_playlist(self, playlist_id):
        url = uapi.playlist_api.format(playlist_id)
        try:
            data = tools.curl(url, self.__headers)
            playlist = data['result']
            return playlist
        except Exception as e:
            raise

    def get_target_r(self, obj, limit_r=default_r):
        max_valid = max([x['br'] for x in obj['brs']])
        return limit_r if max_valid > limit_r else max_valid

    def view_down(self, mv_id, path=".", r=default_r):
        detail = self.get_mv_detail(mv_id=mv_id)
        target_r = self.get_target_r(detail, r)
        link = self.get_mv_link(mv_id, target_r)
        pylog.print_info(
            "正在下载MV {}-{}.mp4".format(
                tools.encode(detail['name']),
                tools.encode(detail['artistName'])
            )
        )

        req = requests.get(link)
        with open("{}/{}-{}{}".format(
                path,
                tools.encode(detail['artistName']).replace("/", "-"),
                tools.encode(detail['name']).replace("/", "-"),
                ".mp4"
        ).decode('utf-8'), "wb") as code:
            code.write(req.content)

        pylog.print_warn("下载成功")

    def get_mv_detail(self, mv_id):
        obj = {'id': mv_id, 'csrf_token': 'csrf'}
        data = {
            'params': create_params_by_dict(obj),
            'encSecKey': self.__encSecKey
        }
        url = uapi.mv_detail_url
        try:
            req = requests.post(
                url, headers=self.__headers, data=data, timeout=10
            ).json()
            if req['code'] == 200:
                return req['data']
        except Exception as e:
            raise

    def get_mv_link(self, mv_id, r):
        obj = {'id': mv_id, 'r': r, 'csrf_token': 'csrf'}
        data = {
            'params': create_params_by_dict(obj),
            'encSecKey': self.__encSecKey
        }
        url = uapi.mv_url
        try:
            req = requests.post(
                url, headers=self.__headers, data=data, timeout=10
            ).json()
            if req['code'] == 200:
                return req['data']['url']
        except Exception as e:
            raise
