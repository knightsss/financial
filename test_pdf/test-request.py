#coding=utf-8
__author__ = 'shifx'

import json,urllib2,urllib
import requests,simplejson

#定义请求头
header_dict = {
        'Host':'www.cninfo.com.cn',
        'Referer':'http://www.cninfo.com.cn/cninfo-new/announcement/show',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": 'http://www.cninfo.com.cn',
        "Proxy-Connection":'keep-alive',
    }

def juchao_request(search_date, page_number):
    textmod={
        "column": "szse",
        "columnTitle":"历史公告查询",
        "pageNum":1,
        "pageSize": 30,
        "tabName":'fulltext',
        "seDate":'2018-01-02',
    }

    url='http://www.cninfo.com.cn/cninfo-new/announcement/query'
    r = requests.post (url, data = textmod, headers = header_dict)
    return r.content

import datetime
if __name__ == '__main__':
    # test_url()
    #构造日期
    current_year = 2018
    next_year = current_year + 1
    current_date = datetime.datetime(current_year, 1, 1)
    next_year_date = datetime.datetime(next_year, 1, 1)
    last_date = next_year_date - datetime.timedelta(days=1)

    #遍历当年的每一天
    while(current_date<=last_date):
        search_date = current_date.strftime('%Y-%m-%d')
        #获取第一页信息,求出总页数
        contens = juchao_request(search_date,1)
        json_content = simplejson.loads(contens)
        total_count = json_content['totalRecordNum']
        page_count = (total_count+29)/30
        print "total_count:",total_count
        print "page_count:",page_count
        print contens

        #遍历当天的所有page
        for i in range(page_count):
            page_number = i + 1
            search_content = juchao_request(search_date, page_number)
            json_search_content = simplejson.loads(search_content)
            #遍历每一个page的30条信息
            for message in json_search_content['announcements']:
                announcement_id = message['announcementId']
                adjunct_url = message['adjunctUrl']
                announcementTime = message['announcementTime']
                adjunct_type = message['adjunctType']
                sec_name = message['secName']
                announcement_title = message['announcementTitle']
                org_id = message['orgId']
                sec_code = message['secCode']
                adjunct_size = message['adjunctSize']
                pdf_url = 'http://www.cninfo.com.cn/' + adjunct_url

                #获取pdf大小、页数

                print search_date,' ',announcement_id,'  ',sec_code,'   ',sec_name,'  ' ,announcement_title,'   ',pdf_url,' ',adjunct_size
            break
        break
        current_date = current_date + datetime.timedelta(days=1)