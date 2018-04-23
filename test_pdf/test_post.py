#coding=utf-8
__author__ = 'shifx'

import json,urllib2,urllib
import requests,simplejson
import datetime

def test_url():
    textmod={
        "column": "szse",
        "columnTitle":"历史公告查询",
        "pageNum":1,
        "pageSize": 300,
        "tabName":'fulltext',
        "seDate":'2001-03-01 ~ 2002-03-14',
    }
    # textmod = json.dumps(textmod)
    test_data_urlencode = urllib.urlencode(textmod)
    # print test_data_urlencode
    # print(textmod)
    #输出内容:{"params": {"password": "zabbix", "user": "admin"}, "jsonrpc": "2.0", "method": "user.login", "auth": null, "id": 1}
    header_dict = {
        'Host':'www.cninfo.com.cn',
        'Referer':'http://www.cninfo.com.cn/cninfo-new/announcement/show',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        "Content-Type": "application/json",
        "Origin": 'http://www.cninfo.com.cn',
        "Connection":'keep-alive',
    }
    url='http://www.cninfo.com.cn/cninfo-new/announcement/query'
    req = urllib2.Request(url,test_data_urlencode,header_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    # print(res)

def test_request():
    textmod={
        "column": "szse",
        "columnTitle":"历史公告查询",
        "pageNum":1,
        "pageSize": 30,
        "tabName":'fulltext',
        "seDate":'2001-03-01 ~ 2002-03-14',
    }
    header_dict = {
        'Host':'www.cninfo.com.cn',
        'Referer':'http://www.cninfo.com.cn/cninfo-new/announcement/show',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": 'http://www.cninfo.com.cn',
        "Proxy-Connection":'keep-alive',
    }
    url='http://www.cninfo.com.cn/cninfo-new/announcement/query'
    r = requests.post (url, data = textmod, headers = header_dict)
    return r.content

if __name__ == '__main__':
    # test_url()

    #测试使用
    contens = test_request()
    json_content = simplejson.loads(contens)
    for i in json_content['announcements']:
        print i['secName']
    print json_content['announcements'][0]
    print len(json_content['announcements'])

    #循环
    current_year = 2017
    next_year = current_year + 1
    current_date = datetime.datetime.strptime('2017-01-02 12:23:55', "%Y-%m-%d %H:%M:%S")
    print current_date
    # while