#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import platform
from Download import request
from pymongo import MongoClient
import datetime

class mzitu():

    def __init__(self):
        # self.headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        # }
        # 获取当前目录
        self.src = ''
        if platform.system() == 'Windows':
            self.src = os.getcwd() + "\\src"
        else:
            self.src = os.getcwd()+'/src'

        client = MongoClient()
        db = client['meinvxiezhenji']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []


    # 获取所有的链接
    def all_url(self, url):
        # html = self.request(url)
        html = request.get(url, 3)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', attrs={'class': 'all'}).find_all('a')
        # 页面上多了一个早期图片，删除了
        all_a.pop(0)
        for a in all_a:
            title = a.get_text()
            print('开始保存: ', title)
            self.title = title
            path = str(title).replace(":", "")
            self.mkdir(path)
            href = a['href']
            self.url = href #将页面地址保存到self.url中
            if self.meizitu_collection.find_one({'主题页面': href}):
                print(u'这个页面已经爬取过了')
            else:
                self.html(href)

    def html(self, href):
        # html = self.request(href)
        html = request.get(href, 3)
        max_page = BeautifulSoup(html.text, 'lxml').find('div', 'pagenavi').find_all('span')[-2].get_text().strip()
        # self.update_header(href)
        page_num = 0
        for page in range(1, int(max_page) + 1):
            page_num = page_num + 1
            print('正在下载第{}张图片'.format(page))
            page_url = href + '/' + str(page)
            self.img(page_url,  max_page, page_num, referer=href)

    # 处理套图地址获得图片的页面地址
    def img(self, page_url, max_page, page_num, referer):
        # img_html = self.request(page_url)
        img_html = request.get(page_url, 3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', attrs={'class': 'main-image'}).find('img')['src']
        self.img_urls.append(img_url)
        if int(max_page) == page_num:
            self.download_img(img_url, referer)
            post = {
                '标题': self.title,
                '主题页面': self.url,
                '图片地址': self.img_urls,
                '获取时间': datetime.datetime.now()
            }
            self.meizitu_collection.insert_one(post)
            print(u'插入数据库成功')
        else:
            self.download_img(img_url, referer)

    def download_img(self, img_url, referer):
        name = img_url[-9:-4] + '.jpg'
        # img = self.request(img_url)
        img = request.get(img_url, 3, referer=referer)
        with open(name, 'wb') as f:
            f.write(img.content)

    # 用于创建文件夹
    def mkdir(self, path):
        path = os.path.join(self.src, path.strip())
        if not os.path.exists(path):
            os.makedirs(path)
            os.chdir(path)

    # 获取网页的 response 然后返回
    def request(self, url):
        content = requests.get(url, headers=self.headers)
        return content

    # 绕过反爬虫机制
    def update_header(self, referer):
        self.headers['Referer'] = '{}'.format(referer)

Mzitu = mzitu()
Mzitu.all_url('https://www.mzitu.com/all/')