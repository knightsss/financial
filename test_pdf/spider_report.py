#coding=utf-8
__author__ = 'shifx'
import math
import time
import urllib2
import re
import os
from bs4 import BeautifulSoup

import requests

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'istock.jrj.com.cn',
        'Referer':'http://istock.jrj.com.cn/yanbao_1_p2.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}
#获取最基础的报告类型url ---公司研究 行业研究
def get_base_report_type_url():
    base_report_type_url_list = []
    report_dict = {}
    report_dict['report_type_id'] = 1
    report_dict['report_type'] = '宏观研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_1.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 2
    report_dict['report_type'] = '行业研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_2.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 3
    report_dict['report_type'] = '公司研究'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_3.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 8
    report_dict['report_type'] = '策略趋势'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_8.html'
    base_report_type_url_list.append(report_dict)

    report_dict = {}
    report_dict['report_type_id'] = 9
    report_dict['report_type'] = '券商晨会'
    report_dict['report_url'] = 'http://istock.jrj.com.cn/yanbao_9.html'
    base_report_type_url_list.append(report_dict)

    return base_report_type_url_list

# open the url and read
def get_html(url):
    # page = urllib2.request.urlopen(url)
    # page = urllib2.urlopen(url)

    # response = requests.get(url,headers=headers)
    # print type(response.content)
    # html = response.content
    get_html_flag = True
    count = 0
    while get_html_flag:
        try:
            req = urllib2.Request(url = url)
            print "open"
            page = urllib2.urlopen(req)
            html = page.read()
            page.close()
            get_html_flag = False
        except:
            time.sleep(3)
            print "spider error..."
            if count > 2:
                get_html_flag = False
        count = count + 1
    return html

def get_page_count_soup(base_report_type_url):
    base_report_type_url = base_report_type_url.replace('.html','_p' + str(661) + '.html')
    html = get_html(base_report_type_url)
    # print html
    print base_report_type_url
    print "get html ok"
    time.sleep(1)
    soup = BeautifulSoup(html,"html.parser")
    # print soup.find(class_='yb_con')
    # print soup.find(class_='page')
    page_count = int(soup.find(class_='page').find('span').string)
    return page_count

    # elements = soup.find(class_='yb_con').find_all('li')
    # for elem in elements:
    #     a_element = elem.find('a')
    #     if a_element != None:
    #         base_url_list.append(a_element['href'])
    #         print a_element['title']
#基于每一页的url,获取当页的所有report的地址
def get_article_url_list(base_url):

    f = open("test.txt","w")
    base_html = get_html(base_url)
    base_url_list = []
    soup = BeautifulSoup(base_html,"html5lib")
    elements = soup.find(class_='yb_con').find_all('li')
    for elem in elements:
        elem_dict = {}
        a_element = elem.find('a')
        print "a_element", a_element
        if a_element != None:
            elem_dict['title'] = unicode(a_element['title']).encode('utf-8')
            report_organization, report_title = zhongwen_cute(elem_dict['title'])
            elem_dict['report_organization'] = report_organization
            elem_dict['report_title'] = report_title
            elem_dict['url'] = a_element['href']
            elem_dict['time'] = unicode(elem.find('span').string).encode('utf-8')
            elem_dict['date'] = elem_dict['time'].split(' ')[0].replace('-','')
            elem_dict['file_name'] = 'qsyb' + str(elem_dict['date']) + '#' + elem_dict['url'][-12:-5] + '.pdf'
            print elem_dict['date'], '  ',elem_dict['file_name']
            f.write(elem_dict['title'])
            f.write('\n')
            f.write(elem_dict['url'])
            f.write('\n')
            f.write(elem_dict['date'])
            f.write('\n')
            elem_dict['url'] = a_element['href']
            elem_dict['date'] = elem.find('span').string
            print a_element.string
            print elem.find('span').string
            base_url_list.append(elem_dict)
            # print a_element['title']
    return base_url_list

#基于report地址，获取pdf地址，pdf文件名，报告内容
def get_report_message(report_url):
    print "report_url",report_url
    article_html = get_html(report_url)
    print article_html
    soup = BeautifulSoup(article_html,"html.parser")
    main_element = soup.find(class_='main')
    print main_element
    main_content =  main_element.find('div').strings
    contents = ''
    for content in main_content:
        contents = contents + content

    pdf_url = main_element.find('a')['href']
    pdf_name = main_element.find('a').string
    print "title:",soup.find(class_='tit').find(class_='fl').string
    print "contents:",contents
    print "pdf_url:",main_element.find('a')['href']
    print "pdf_name:",main_element.find('a').string
    return pdf_url,pdf_name,contents

def zhongwen_cute(words):
    report_word = words.split('--')
    report_organization = report_word[0]
    report_title = report_word[1].split('【')[0]
    print "report_organization:",report_organization
    print "report_title:",report_title
    return report_organization, report_title


if __name__ == '__main__':
    #获取基础对象
    base_report_type_url_list = get_base_report_type_url()
    #遍历5大类
    # for base_report_type_url in base_report_type_url_list:
    #     print base_report_type_url['report_url']
    #     page_count = get_page_count_soup(base_report_type_url['report_url'])
    #     print "report_type:", base_report_type_url['report_type'] ," page count:",page_count

    #获取page_count
    base_report_type_url = base_report_type_url_list[0]['report_url']
    page_count = get_page_count_soup(base_report_type_url)

    #访问mysql  获取mysql总记录数
    mysql_count = 49
    last_time = '2010-03-06 12:34:44'

    start_page_number = int(page_count - math.floor((mysql_count)/50))
    print start_page_number

    #构造page url
    page_url_list = []
    for i in range(start_page_number):
        page_number = start_page_number - i
        report_type_url = base_report_type_url.replace('.html','_p' + str(page_number) + '.html')
        page_url_list.append(report_type_url)
    print len(page_url_list)
    print page_url_list[0],page_url_list[-1]

    #通过page url获取所有报告地址
    base_url = page_url_list[0]
    report_url_list = get_article_url_list(base_url)
    for report_url in report_url_list:
        print report_url

    #通过report 地址获取详细信息
    # pdf_url,pdf_name,contents = get_report_message(report_url_list[-1])
    print '--------------------------------------'

    pdf_url,pdf_name,contents = get_report_message('http://istock.jrj.com.cn/article,yanbao,7474954.html')


