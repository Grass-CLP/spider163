#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/16.
# email to LipsonChan@yahoo.com
#
import json

from spider163.spider.mv import MV, r_240p

mv = MV()
link = mv.get_mv_link(5324139, 720)
detail = mv.get_mv_detail(5324139)
mv.view_down(5324139, r=r_240p)

print(link)
print(json.dumps(detail))
