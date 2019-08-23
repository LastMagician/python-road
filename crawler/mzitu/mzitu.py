#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

class mzitu():

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        # 获取当前目录
        self.src = os.getcwd() + "\\src"

    # 获取所有的链接
    def all_url(self, url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', attrs={'class': 'all'}).find_all('a')
        # 页面上多了一个早期图片，删除了
        all_a.pop(0)
        for a in all_a:
            title = a.get_text()
            print('开始保存: ', title)
            path = str(title).replace(":", "")
            self.mkdir(path)
            href = a['href']
            self.html(href)

    def html(self, href):
        html = self.request(href)
        max_page = BeautifulSoup(html.text, 'lxml').find('div', 'pagenavi').find_all('span')[-2].get_text().strip()
        self.update_header(href)
        for page in range(1, int(max_page) + 1):
            print('正在下载第{}张图片'.format(page))
            page_url = href + '/' + str(page)
            self.img(page_url)

    # 处理套图地址获得图片的页面地址
    def img(self, page_url):
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', attrs={'class': 'main-image'}).find('img')['src']
        self.download_img(img_url)

    def download_img(self, img_url):
        name = img_url[-9:-4] + '.jpg'
        img = self.request(img_url)
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
#
# # 创建并切换目录
# def chdir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)
#
# # 下载图片
# def download_img(url, img_src, img_url):
#     update_header(img_url)
#     name = img_url[-9:-4]
#     html = requests.get(img_url, headers=header)
#     with open(name, 'wb') as f:
#         f.write(html.content)
#
# def request(url):
#     header = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#     }
#     content = requests.get(img_url, headers=header)
#     return content
#
# daily_url = 'https://www.mzitu.com/all/'
# # 请求每日更新数据
# daily_html = requests.get(daily_url, headers=header)
# daily_soup = BeautifulSoup(daily_html.content, 'lxml')
# # 解析网页数据，获取所有页面链接
# daily_content = daily_soup.find('div', attrs={'class': 'all'}).find_all('a')
# # 删除第一个无用数据
# daily_content.pop(0)
# for item in daily_content:
#     # 标题
#     title = item.get_text()
#     # 页面链接
#     href = item['href']
#     # 删除可能对目录名称造成影响的符号
#     title = title.replace(':', ' ')
#     # 创建并切换目录
#     chdir(src + title)
#     img_html = requests.get(href, headers=header)
#     img_soup = BeautifulSoup(img_html.content, 'lxml')
#     # 解析获取图片数量
#     lastpage = img_soup.find('div', attrs={'class': 'pagenavi'}).find_all('a')[-2].get_text().strip()
#     # 构造图片主页链接
#     for page in range(1, int(lastpage)+1):
#         img_html = requests.get(href+'/'+str(page), headers=header)
#         img_soup = BeautifulSoup(img_html.content, 'lxml')
#         img_url = img_soup.find('div', attrs={'class': 'main-image'}).find_all('img')[0]['src']
#         # 下载图片
#         print('正在下载{}的第{}张图片'.format(title, page))
#         download_img(href, src + title + '\\' + img_url[-9:-4] + '.jpg', img_url)