#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time    : 18-12-7 下午10:34
# @Author  : ylin
# Description:
# scrap bilibili video,need config cookie(file),the aid of the video series,and save path.
import json
import os
import re
import threading

import requests

headers_file = 'headers'
cookie_file = 'cookie'
default_aid = '35932863'
default_save = '/run/media/ylin/Elements/vedio/machine_learning_2019/'


def cut(file):
    with open(file, 'r')as f:
        lines = f.readlines()
        head = dict()
        for x in range(0, int(len(lines) / 2)):
            head[lines[2 * x].strip()] = lines[2 * x + 1].strip()
    return head


class Scraper:
    def __init__(self, save_path=default_save, aid=default_aid):
        self.save_to = save_path
        self.aid = aid
        self.s = requests.session()
        self.s.headers = cut(headers_file)
        # Visit the main video source page,here we can get the page_id of all branch source.
        r = self.s.get('https://www.bilibili.com/video/av{}'.format(aid))
        self.video_data = json.loads('[' + re.findall('"pages":\[(.*?)\]', r.text)[0] + ']')
        self.s.headers['Host'] = 'api.bilibili.com'
        self.s.headers['Referer'] = 'https://www.ibilibili.com/video/av{}'.format(aid)

    def travel_source(self, mode):
        if mode == 'save':
            print('star saving...')
            target = self.save
        else:
            print('star checking...')
            target = self.check
        for x in self.video_data:
            url = 'https://api.bilibili.com/playurl?' \
                  'callback=callbackfunction&aid={}&page={}&' \
                  'platform=html5&quality=1&vtype=mp4&type=jsonp&_=1544262035067' \
                .format(self.aid, x['page'])
            self.s.headers['Cookie'] = cut(cookie_file)['Cookie']
            r = self.s.get(url)
            url = json.loads(re.findall('callbackfunction\((.*?)\)', r.text)[0])['durl'][0]['url']
            threading.Thread(target=target, args=(re.sub('[ \-:,"“”!?]+', '_', x['part']) + '.mp4', url)).start()  #

    def save(self, name, url):
        print('downloading ' + name)
        # os.system('wget -O "{}" "{}"'.format(save_to + name, url))
        if name not in os.listdir(self.save_to):
            with open(self.save_to + name, 'wb')as fp:
                r = self.s.get(url)
                # print(r.content)
                fp.write(r.content)
            print('\n' + name, '\nsave successfully')
        else:
            print('\n' + name, '\nis already in your directory')

    def check(self, *args):
        name = args[0]
        if name not in os.listdir(self.save_to):
            print('\n' + name, '\nsave successfully')
        else:
            print('\n' + name, '\nis already in your directory')


if __name__ == '__main__':
    Scraper().travel_source('check')
    pass
