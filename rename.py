#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 18-12-9 上午10:21
# @Author  : ylin
# Description:
#
import re

from gevent import os


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        if file != 'machine_learning_2019' and file != 'part_2':
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                listdir(file_path, list_name)
            else:
                # print(re.sub('[ \-:,"“”!?_]+', '_', file_path))
                file_path2 = re.sub('[ \-:,"“”!_]+', '_', file_path)
                os.rename(file_path, file_path2)
                # file_path=re.sub('[ \-:,"“”!]', '_', file_path) + '.mp4'
                # list_name.append(file_path)


if __name__ == '__main__':
    save_to = '/run/media/ylin/Elements/vedio/'
    # w = os.walk(save_to)
    # for r, d, f in w:
    #     for x in f:
    #         print(re.sub('[ \-:,"“”!]', '', x) + '.mp4')
    list_name = []
    listdir(save_to, list_name)
    # print(list_name)

    pass
