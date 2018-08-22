# !/user/bin/env python
# -*- coding:utf-8 -*- 
__author__ = 't.s.helianthus'

'''
内容:爬取IT桔子中的各大公司详情
目标网址:http://radar.itjuzi.com/company
'''

import requests,time,re,random
import pandas as pd
from pandas.io.json import json_normalize  
import os
import time
import random
import urllib
import numpy as np
import pymysql
from bs4 import BeautifulSoup
import math

os.chdir('F:\CBNweekly\Code\output\company\it_orange')


cookie_body = '_ga=GA1.2.1531152702.1534234070; gr_user_id=91d9426a-6e5e-4124-aa1b-2ae8aa5d97b2; MEIQIA_EXTRA_TRACK_ID=18mLyhibeZOO2ro9vtCyfcPlVhH; _gid=GA1.2.1670999455.1534350111; acw_tc=AQAAAETRBXNEQwoAvzzBtzGmhpyI6975; paidtype=vip; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1534234789,1534394372,1534522312; MEIQIA_VISIT_ID=18vm8jEhEoOPofgMX8sg3UQx7Xs; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1534439647,1534501497,1534522289,1534524588; gr_cs1_72796a86-e77c-4e3b-a73f-d646e7f4779e=user_id%3A619414; gr_session_id_eee5a46c52000d401f969f4535bdaa78=709491f8-5982-4c04-a432-b2b6630d339b; gr_session_id_eee5a46c52000d401f969f4535bdaa78_709491f8-5982-4c04-a432-b2b6630d339b=true; identity=datavisual%40163.com; unique_token=619414; gr_cs1_709491f8-5982-4c04-a432-b2b6630d339b=user_id%3A619414; session=08e75a3b0cb16189eefd0f3c0f98d0009faa1507; remember_code=bWGIAamq96; user-radar.itjuzi.com=%7B%22n%22%3A%22datavisual%22%2C%22v%22%3A3%7D; _gat=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1534527519; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1534527520'
company_table = []
province_name = "陕西"
province_str = urllib.parse.quote(province_name)
page = page_all = 1
while page <= page_all:
    url = 'http://radar.itjuzi.com/company/infonew?page={}&prov%5B%5D={}'.format(str(page), province_str)
    #必须带上cookie才行
    head = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'gr_user_id=f4e1ff74-cca6-4f8b-8455-6201b8b952f6; acw_tc=AQAAANAfFgVfnQEA6krX31zNMf57uigb; identity=1073064953%40qq.com; remember_code=hBezMtQFUE; unique_token=529615; paidtype=vip; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1521860671; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1521950090; session=c8bf1e4c0aee0596cfc36e65e9fb92e870b2ac6c; user-radar.itjuzi.com=%7B%22n%22%3A%22%5Cu6854%5Cu53cb3c38bf2e9843e%22%2C%22v%22%3A2%7D; gr_session_id_eee5a46c52000d401f969f4535bdaa78=5331ade4-7812-4b73-ba7e-c505537aaaa8; gr_cs1_5331ade4-7812-4b73-ba7e-c505537aaaa8=user_id%3A529615; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1521860750; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1521955860; _ga=GA1.2.1041203472.1521860671; _gid=GA1.2.1400073980.1521860671; _gat=1; MEIQIA_EXTRA_TRACK_ID=12FqHHK1WnlIgT0BMyeZvSNMFjh',
    'Referer':'http://radar.itjuzi.com/company',
    'Host':'radar.itjuzi.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }
    head['Cookie'] = cookie_body
    html = requests.get(url,headers=head).json()
    print( html['data']['page_num'])
    time.sleep(random.randint(0,9))
    company = html['data']['rows']
    if page == 1:
        page_all = html['data']['page_total']
    time.sleep(random.randint(60, 120))
    [company_table.append(i) for i in company]
    page = page + 1
company_t = pd.DataFrame(company_table)
csv_file = '#it_orange#%s_startup-1.0(2018).csv' % (province_name)
company_t.to_csv(csv_file,encoding='UTF-8')

def down_detail(com_id,):
    com_id = str(com_id)
    file_name = com_id + '.txt'
    try:
        f = open(''+file_name, encoding = 'UTF-8')
        html = f.read()
    except:
        time.sleep(random.randint(0,9))
        print('down:', com_id)
        url = 'https://www.itjuzi.com/company/' + str(com_id)
        # print(url)
        head = {
            'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host':'www.itjuzi.com',
            'Pragma': 'no-cache',
            # 'Referer': 'https://www.itjuzi.com/company/32756882',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/55.0.2883.87Safari/537.36'
        }
        head['Cookie'] = cookie_body
    
        html = requests.get(url,headers=head).text
        if len(html)>1:
            file_name = com_id + '.txt'
            f = open(''+file_name,'w', encoding='utf-8')
            f.write(html)
            f.close()
    print(html[90:100])
    return(html)


province_name = "shanxi"
csv_file = 'F:\CBNweekly\Code\output\company\it_orange\#it_orange#%s_startup-1.0(2018).csv' % (province_name)
company_base = pd.read_csv(csv_file, encoding = 'UTF-8')

table_name_body = 'du_startup_it_orange'
insert_field = [column for column in company_base]
insert_field.pop(0)

# connect
rising = {'host':'172.24.30.0', 'port':3306, 'user':'iiiiiiiiii', 'password':'iiiiiiiiiiiiii'}
con_rising = pymysql.connect(host=rising['host'], user=rising['user'], passwd=rising['password'], db='risingdata', port=rising['port'],charset='utf8')
insertTable(insert_table = company_base, table_name = table_name_body, insert_field = insert_field, id = ['com_id'], connect = con_rising)
con_rising.close() # 释放数据库资源


com_id_list = company_base['com_id']

i = 0
total = len(com_id_list)
#total = 10
company_table = []
for i in range(i, total ):
    com_id = str(com_id_list[i])
    webpage = down_detail(com_id = com_id)
    soup = BeautifulSoup(webpage, 'lxml')
    tags = ','.join([i.get_text() for i in soup.select(' div.tagset.dbi.c-gray-aset.tag-list > a')])
    about_us =  [i.get_text() for i in soup.select('ul.list-block.aboutus > li > span')]
    if (len(about_us) == 0):
        address = 'NA'
    else:
        address = about_us[len(about_us)-1]
        address = address[0:len(address)-1]

    temp = {"com_name":soup.find_all('h1')[0].get('data-name') ,
     "address":address,
     "entName": soup.find_all('h1')[0].get('data-fullname'),
     "seo_slogan":soup.select('h2.seo-slogan')[0].get_text(),
     #"website": soup.select('div.link-line > a ')[2].get('href'),
     "tags":tags,
     "com_id":com_id}
    
    company_table.append(temp)

company_add = pd.DataFrame(company_table)

con_rising = pymysql.connect(host=rising['host'], user=rising['user'], passwd=rising['password'], db='risingdata', port=rising['port'],charset='utf8')
update_field = [column for column in company_add]
updateTable(update_table = company_add, table_name = table_name_body, update_id = 'com_id', update_field = update_field, connect = con_rising)
con_rising.close() # 释放数据库资源
