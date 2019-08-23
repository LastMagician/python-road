#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

# 构造请求头
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# 获取当前目录
src = os.getcwd() + "\\src\\"

# 绕过反爬虫机制
def update_header(referer):
    header['Referer'] = '{}'.format(referer)

# 创建并切换目录
def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 下载图片
def download_img(url, img_src, img_url):
    update_header(img_url)
    html = requests.get(img_url, headers=header)
    with open(img_src, 'wb') as f:
        f.write(html.content)

def get_html(url, headers):
    html = requests.get(img_url, headers=headers)
    if html.status_code == 200:
        return html.content
    else:
        return str(html.status_code) + ',' + html.text

daily_url = 'https://www.mzitu.com/all/'
# 请求每日更新数据
daily_html = requests.get(daily_url, headers=header)
daily_soup = BeautifulSoup(daily_html.content, 'lxml')
# 解析网页数据，获取所有页面链接
daily_content = daily_soup.find('div', attrs={'class': 'all'}).find_all('a')
# 删除第一个无用数据
daily_content.pop(0)
for item in daily_content:
    # 标题
    title = item.get_text()
    # 页面链接
    href = item['href']
    # 删除可能对目录名称造成影响的符号
    title = title.replace(':', ' ')
    # 创建并切换目录
    chdir(src + title)
    img_html = requests.get(href, headers=header)
    img_soup = BeautifulSoup(img_html.content, 'lxml')
    # 解析获取图片数量
    lastpage = img_soup.find('div', attrs={'class': 'pagenavi'}).find_all('a')[-2].get_text().strip()
    # 构造图片主页链接
    for page in range(1, int(lastpage)+1):
        img_html = requests.get(href+'/'+str(page), headers=header)
        img_soup = BeautifulSoup(img_html.content, 'lxml')
        img_url = img_soup.find('div', attrs={'class': 'main-image'}).find_all('img')[0]['src']
        # 下载图片
        print('正在下载{}的第{}张图片'.format(title, page))
        download_img(href, src + title + '\\' + img_url[-9:-4] + '.jpg', img_url)