#coding=utf-8
__author__ = 'shifx'
import os
import time
import urllib2

def get_page(url):
    # page = urllib2.request.urlopen(url)
    get_html_flag = True
    count = 0
    while get_html_flag:
        try:
            req = urllib2.Request(url = url)
            page = urllib2.urlopen(req, timeout=10)
            get_html_flag = False
        except:
            print "spider page again..."
            if count > 0:
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
    path_file_name = '/home/user1/python/report/file/' + file_name
    # print "file_name",file_name
    page = get_page(url)
    if page == '':
        print ("faild to download" + " " + path_file_name)
        return False
    else:
        try:
            f = open(path_file_name, 'wb')
            block_sz = 8192
            while True:
                buffer = page.read(block_sz)
                if not buffer:
                    break
                f.write(buffer)
            f.close()
        except:
            print ("faild to download" + " " + path_file_name)
            return False
        print ("Sucessful to download" + " " + path_file_name)
        return True

from PyPDF2 import PdfFileReader, PdfFileWriter
#获取文件页数，文件大小
def reload_pdf(file_name):
    # 获取一个 PdfFileReader 对象
    page_count = 0
    file_size = 0
    path_file_name = '/home/user1/python/report/file/' + file_name
    try:
        pdf_input = PdfFileReader(open(path_file_name, 'rb'))
        # 获取 PDF 的页数
        page_count = pdf_input.getNumPages()
    except:
        page_count = 0
    try:
        file_size = get_FileSize(path_file_name)
    except:
        file_size = 0
    return page_count,file_size

def get_FileSize(filePath):
    # filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024)
    return round(fsize)