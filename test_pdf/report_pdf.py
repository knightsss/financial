#coding=utf-8
__author__ = 'shifx'
import os
import time
import urllib2
from bs4 import BeautifulSoup

def get_page(url):
    # page = urllib2.request.urlopen(url)
    get_html_flag = True
    count = 0
    while get_html_flag:
        try:
            req = urllib2.Request(url = url)
            print "open"
            page = urllib2.urlopen(req)
            get_html_flag = False
        except:
            time.sleep(3)
            print "spider again..."
            if count > 2:
                get_html_flag = False
                print "spider error..."
                page = ''
        count = count + 1
    return page

def get_pdf_path():
    pwd = os.getcwd()
    print pwd
    father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    print father_path
    return father_path

def download_pdf(url,file_name):
    # url = "http://pg.jrj.com.cn/acc/Res/CN_RES/FUTURES/2018/3/1/4ae0f0c1-72c1-441c-8315-f21f6366216a.pdf"
    print "pdf url ",url
    # file_name = get_pdf_path() + "\\research_report_pdf\\" + file_name
    print "file_name",file_name
    page = get_page(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = page.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)

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

def get_report_message(report_url):
    print "report_url",report_url
    article_html = get_html(report_url)
    # print article_html
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


if __name__ == '__main__':
    # pdf_url,pdf_name,contents = get_report_message('http://istock.jrj.com.cn/article,yanbao,7474954.html')

    pdf_url,pdf_name,contents = get_report_message('http://istock.jrj.com.cn/article,yanbao,6826457.html')
    download_pdf(pdf_url,'we34#wew.pdf')