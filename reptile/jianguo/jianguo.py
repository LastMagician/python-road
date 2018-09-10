#! /usr/bin/env python3 
# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import re

browser = webdriver.Chrome()
# 设置网站等待时间
wait = WebDriverWait(browser, 5)

# 获取源码
def get_one(url):
    print('正在爬取中...')
    try:
        browser.get(url)
        html = browser.page_source
        if html:
            return html
    except EOFError:
        return None

# 保存图片（以 jpg 的格式）
def write_file(url, num, count):
    dirName = u'{}/{}'.format('images', num)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, count)
    with open(filename, 'wb+') as jpg:
        jpg.write(requests.get(url).content)

# 源码处理
def html_parseone(html):     
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select('.commentlist  img')
    url = soup.select('#body .current-comment-page')    
    current_num = re.findall('\d+', str(url))[0]
    
    count = 0
    for img in imgs:
        img_url = re.findall('src="(.*?)"', str(img))
        if not img_url[0][-3:] == 'gif':
            if not img_url[0][-3:] == 'png':
                print('正在下载：%s 第 %s 张' % (img_url[0], count))                
                write_file(img_url[0], current_num, count)
        count += 1

    next_num = int(current_num) - 1
    next_url = 'https://jandan.net/ooxx/page-%s#comments' % (next_num)
    
    return next_url, next_num

# 循环获取图片
def next(url, num):
    while int(num) > 0:
        html = get_one(url)
        url, num = html_parseone(html)

def main():
    url = 'https://jandan.net/ooxx'
    html = get_one(url)
    next_url, page_num = html_parseone(html)
    next(next_url, page_num)
    
if __name__ == '__main__':
    main()