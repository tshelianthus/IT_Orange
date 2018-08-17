# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/25--13:10
__author__ = 'Henry'

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
cookie_body = '_ga=GA1.2.1531152702.1534234070; gr_user_id=91d9426a-6e5e-4124-aa1b-2ae8aa5d97b2; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1534234072; MEIQIA_EXTRA_TRACK_ID=18mLyhibeZOO2ro9vtCyfcPlVhH; identity=xiangweixiao%40163.com; remember_code=.lFZcxZoVP; unique_token=616796; _gid=GA1.2.1670999455.1534350111; session=6c0e7f02e1a1090ea8f9fc099a0df06d18e80bbc; acw_tc=AQAAAIrr415KkQsAgxFE3nmcM8OaLOsZ; user-radar.itjuzi.com=%7B%22n%22%3A%22helianthus%22%2C%22v%22%3A2%7D; gr_session_id_eee5a46c52000d401f969f4535bdaa78=4e5aacc6-144f-429f-b31c-9766ee2ceb56; gr_cs1_4e5aacc6-144f-429f-b31c-9766ee2ceb56=user_id%3A616796; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1534234789,1534394372; gr_session_id_eee5a46c52000d401f969f4535bdaa78_4e5aacc6-144f-429f-b31c-9766ee2ceb56=true; MEIQIA_VISIT_ID=18rarvHYAEunufJq61M86xryfHC; _gat=1; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1534394435'
page = 117
company_table = []
for i in range(1,page+1):
    url = 'http://radar.itjuzi.com/company/infonew?page={}'.format(str(i))
    url = 'http://radar.itjuzi.com/company/infonew?page={}&prov%5B%5D=%E6%B9%96%E5%8C%97'.format(str(i))
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
    # print(html)
    print(i)
    time.sleep(random.randint(0,9))
    company = html['data']['rows']
    time.sleep(random.randint(60, 120))
    [company_table.append(i) for i in company]

company_t = pd.DataFrame(company_table)


company =  spider(117)
# spider(1) --2018-3-26更新6条数据

os.chdir('F:\CBNweekly\Code\output\company\it_orange')

def down_detail(com_id,):
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

    
com_id_t = pd.read_csv('F:\CBNweekly\Code\output\company\it_orange\henan_startup.csv')
com_id_list = com_id_t['x']

for i in range(1,len(com_id_list)-1):
    com_id = str(com_id_list[i])
    file_name = com_id + '.txt'

    try:
        f = open(''+file_name)
        #t = f.read()
        f.close()
        print(com_id)
    except:
        print('down: ' + file_name)
        time.sleep(random.randint(0,9))
        try:
            down_detail(com_id = com_id)
        except:
            time.sleep(random.randint(0,9))
            down_detail(com_id = com_id)