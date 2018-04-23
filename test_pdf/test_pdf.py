#coding=utf-8
__author__ = 'shifx'

import urllib2
import re
import os
from bs4 import BeautifulSoup

from lxml import etree

# open the url and read
def getHtml(url):
    # page = urllib2.request.urlopen(url)
    req = urllib2.Request(url = url)
    page = urllib2.urlopen(req)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)
    url_lst = url_re.findall(html.decode('gb2312'))
    return(url_lst)

def getFile(url):
    file_name = url.split('/')[-1]
    # u = urllib2.Request.urlopen(url)
    req = urllib2.Request(url = url)
    u = urllib2.urlopen(req)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)


def download_self():
    url = "http://pg.jrj.com.cn/acc/Res/CN_RES/FUTURES/2018/3/1/4ae0f0c1-72c1-441c-8315-f21f6366216a.pdf"
    file_name = "self_test2.pdf"
    req = urllib2.Request(url = url)
    u = urllib2.urlopen(req)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)

def get_base_html(url):
    req = urllib2.Request(url = url)
    page = urllib2.urlopen(req)
    html = page.read()
    page.close()
    return html

def get_article_url(base_html):
    base_url_list = []
    soup = BeautifulSoup(base_html)
    elements = soup.find(class_='yb_con').find_all('li')
    for elem in elements:
        a_element = elem.find('a')
        if a_element != None:
            base_url_list.append(a_element['href'])
            print a_element['title']
    return base_url_list


from PyPDF2 import PdfFileReader, PdfFileWriter
def get_article(article_url):
    article_html = get_base_html(article_url)
    soup = BeautifulSoup(article_html)
    main_element = soup.find(class_='main')
    main_content =  main_element.find('div').strings
    contents = ''
    for content in main_content:
        contents = contents + content

    print "title:",soup.find(class_='tit').find(class_='fl').string
    print "contents:",contents
    print "pdf_url:",main_element.find('a')['href']
    print "pdf_name:",main_element.find('a').string

    # selector = etree.HTML(article_html)
    # links = selector.xpath('//*[@id="replayContent"]/p[1]/text()')
    # print "links:",links

    infn = 'http://pg.jrj.com.cn/acc/Res\CN_RES\STOCK\2018\2\28\52281899-021e-4b50-9fd3-4a74703e6e46.pdf'
    outfn = 'self_test.pdf'
    # 获取一个 PdfFileReader 对象
    pdf_input = PdfFileReader(open(outfn, 'rb'))
    # 获取 PDF 的页数
    page_count = pdf_input.getNumPages()
    print page_count




if __name__ == '__main__':
    download_self()
    #http://istock.jrj.com.cn/article,yanbao,30348953.html
    #获取当页的url
    # base_url = 'http://istock.jrj.com.cn/yanbao_3.html'
    # base_html = get_base_html(base_url)
    # base_url_list = get_article_url(base_html)
    # print base_url_list

    #获取文章的具体内容等信息
    article_url = 'http://istock.jrj.com.cn/article,yanbao,30345937.html'
    get_article(article_url)



    # root_url = 'http://www.math.pku.edu.cn/teachers/lidf/docs/textrick/'
    # raw_url = 'http://www.math.pku.edu.cn/teachers/lidf/docs/textrick/index.htm'
    #
    # html = getHtml(raw_url)
    # url_lst = getUrl(html)
    #
    # os.mkdir('ldf_download')
    # os.chdir(os.path.join(os.getcwd(), 'ldf_download'))
    #
    # for url in url_lst[:]:
    #     url = root_url + url
    #     getFile(url)