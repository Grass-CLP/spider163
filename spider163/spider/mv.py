#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from terminaltables import AsciiTable

from spider163 import settings
from spider163.spider import public as uapi
from spider163.spider.common import encSecKey, create_params_by_dict
from spider163.utils import pylog
from spider163.utils import tools

default_r = 720
max_r = default_r


class MV:
    def __init__(self):
        self.__headers = uapi.header
        self.session = settings.Session()
        self.__encSecKey = encSecKey
        self.default_r = 720

    def view_down_(self, playlist_id, path="."):
        list = self.get_playlist(str(playlist_id))
        msg = {"success": 0, "failed": 0, "failed_list": []}
        for music in list['tracks']:
            pylog.print_info(
                "正在下载歌曲 {}-{}.mp3".format(
                    tools.encode(music['name']),
                    tools.encode(music['artists'][0]['name'])
                )
            )
            link = self.get_mv_link(music["id"])
            if link is None:
                msg["failed"] = msg["failed"] + 1
                msg["failed_list"].append(music)
                continue
            r = requests.get(link)
            with open("{}/{}-{}{}".format(
                    path,
                    tools.encode(music['name']).replace("/", "-"),
                    tools.encode(music['artists'][0]['name']).replace("/", "-"),
                    ".mp3"
            ), "wb") as code:
                code.write(r.content)
                msg["success"] = msg["success"] + 1
        pylog.print_warn(
            "下载成功：{} 首，下载失败：{}首".format(msg["success"], msg["failed"])
        )
        tb = [["歌曲名字", "艺术家", "ID"]]
        for music in msg["failed_list"]:
            n = music['name'].encode("utf-8")
            a = music['artists'][0]['name'].encode("utf-8")
            i = music['id']
            tb.append([n, a, i])
        print(AsciiTable(tb).table)

    def get_playlist(self, playlist_id):
        url = uapi.playlist_api.format(playlist_id)
        try:
            data = tools.curl(url, self.__headers)
            playlist = data['result']
            return playlist
        except Exception as e:
            raise

    def get_target_r(self, obj, limit_r=max_r):
        pass

    def view_down(self, mv_id, path=".", r = max_r):
        detail = self.get_mv_detail(mv_id=mv_id)

        list = self.get_playlist(str(playlist_id))
        msg = {"success": 0, "failed": 0, "failed_list": []}
        for music in list['tracks']:
            pylog.print_info(
                "正在下载歌曲 {}-{}.mp3".format(
                    tools.encode(music['name']),
                    tools.encode(music['artists'][0]['name'])
                )
            )
            link = self.get_mv_link(music["id"])
            if link is None:
                msg["failed"] = msg["failed"] + 1
                msg["failed_list"].append(music)
                continue
            r = requests.get(link)
            with open("{}/{}-{}{}".format(
                    path,
                    tools.encode(music['name']).replace("/", "-"),
                    tools.encode(music['artists'][0]['name']).replace("/", "-"),
                    ".mp3"
            ), "wb") as code:
                code.write(r.content)
                msg["success"] = msg["success"] + 1
        pylog.print_warn(
            "下载成功：{} 首，下载失败：{}首".format(msg["success"], msg["failed"])
        )
        tb = [["歌曲名字", "艺术家", "ID"]]
        for music in msg["failed_list"]:
            n = music['name'].encode("utf-8")
            a = music['artists'][0]['name'].encode("utf-8")
            i = music['id']
            tb.append([n, a, i])
        print(AsciiTable(tb).table)

    def get_mv_detail(self, mv_id):
        obj = {'id': mv_id, 'csrf_token':'csrf'}
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

    def get_mv_link(self, mv_id, r=default_r):
        obj = {'id': str(mv_id), 'r': str(r), 'csrf_token': 'csrf'}
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
