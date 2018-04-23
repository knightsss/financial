#coding=utf-8
__author__ = 'shifeixiang'
import urllib2
import time
from bs4 import BeautifulSoup
url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001329252&owner=exclude&action=getcompany&Find=Search'
url2 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001406796&type=&dateb=&owner=exclude&start=0&count=40'


def get_html(url):
    # page = urllib2.request.urlopen(url)
    get_html_flag = True
    count = 0
    while get_html_flag:
        try:
            req = urllib2.Request(url = url)
            page = urllib2.urlopen(req,timeout=15)
            html = page.read()
            page.close()
            get_html_flag = False
        except:
            time.sleep(3)
            print "spider html again..."
            if count > 2:
                get_html_flag = False
                print "spider html error..."
                html = ''
        count = count + 1
    return html

#通过CIK 搜索后页面信息
def get_first_page_info(html):
    soup = BeautifulSoup(html,"html.parser")
    #定义字典存储
    us_dict = {}
    table_list = []

    #处理头部信息
    print "companyInfo:",soup.find(class_='companyInfo')
    mailers = soup.find_all(class_='mailer')
    for mailer in mailers:
        print "mailerAddress:",mailer



    #处理table表信息
    tableFile2 = soup.find(class_='tableFile2')
    table_trs = tableFile2.find_all('tr')

    for table_tr in table_trs:
        tmp_dict = {}
        print "========================"
        #print table_tr
        table_tr_tds = table_tr.find_all('td')
        index = 0
        for table_tr_td in table_tr_tds:
            print "------"
            url = ''
            #print table_tr_td

            if index == 0:
                tmp_dict["filings"] =  unicode(table_tr_td.string).encode('utf-8')
                print table_tr_td.string
                print type(table_tr_td.string)
            #文档地址
            if index == 1:
                url = "http://www.sec.gov/" + table_tr_td.find('a')['href']
                print url
            if index == 2:
                documents_desc = ''
                table_tr_td_strs = table_tr_td.strings
                for table_tr_td_str in table_tr_td_strs:
                    documents_desc = documents_desc + table_tr_td_str
                print documents_desc
            if index == 3:
                print table_tr_td.string
            if index == 4:
                file_num_desc = ''
                table_tr_td_strs = table_tr_td.strings
                for table_tr_td_str in table_tr_td_strs:
                    file_num_desc = file_num_desc + table_tr_td_str + "\n"
                print file_num_desc
            index = index + 1

            if url != '':
                print "url is :",url
                #get_document(url)


#每一个文档页面的信息,一个document对应多个文件
def get_document(url):
    print "+++++++++++++++++++++++++++++++++++++"
    documnet_html = get_html(url)
    if documnet_html == '':
        pass
    else:
        soup = BeautifulSoup(documnet_html,"html.parser")


        #第一栏标题头  和 内容one_title_heads_str  one_title_contents_str
        one_title_heads = soup.find(id="formName").strings
        one_title_heads_str = ''
        for one_title_head in one_title_heads:
            one_title_heads_str = one_title_heads_str + one_title_head.encode('utf-8')

        print "one_title_heads_str:", one_title_heads_str

        one_title_contents = soup.find(id="secNum").strings
        one_title_contents_str = ''
        for one_title_content in one_title_contents:
            one_title_contents_str = one_title_contents_str + one_title_content.encode('utf-8')
        print "one_title_contents_str:",one_title_contents_str


        #第二栏信息处理
        #总共三列，第一列三个，第二列1个或者没有，第三列一个或者没有
        one_content_msgs = soup.find_all(class_="formGrouping")
        for i in range(len(one_content_msgs)):
            if i == 0:
                date_names = one_content_msgs[i].find_all(class_="infoHead")
                date_values = one_content_msgs[i].find_all(class_="info")
                if len(date_values) == 3:
                    filing_date = date_values[0]
                    accepted_date = date_values[1]
                    documents = date_values[2]
                    print "filing_date:",filing_date.string.encode('utf-8')
                    print "accepted_date:",accepted_date.string.encode('utf-8')
                    print "documents:",documents.string.encode('utf-8')
            if i == 1:
                date_values = one_content_msgs[i].find_all(class_="info")
                if len(date_values) == 1:
                    effectiveness_date = date_values[0]
                    print "effectiveness_date:",effectiveness_date.string.encode('utf-8')
            if i == 2:
                date_values = one_content_msgs[i].find_all(class_="info")
                if len(date_values) == 1:
                    items_elements = date_values[0].strings
                    items = ''
                    for items_element in items_elements:
                        items = items + items_element.encode('utf-8')
                    print "items:",items


        #第四栏信息
        #第四栏第一列
        forth_element_company_name_strings = soup.find(class_='companyName').strings
        forth_element_ident_info_strings = soup.find(class_='identInfo').strings

        company_name = ''
        ident_info = ''
        for forth_element_company_name_string in forth_element_company_name_strings:
            company_name = company_name +  unicode(forth_element_company_name_string).encode('utf-8')
        print "company_name:",company_name

        for forth_element_ident_info_string in forth_element_ident_info_strings:
            ident_info = ident_info + unicode(forth_element_ident_info_string).encode('utf-8')
        print "ident_info:",ident_info

        #第四栏第二列/第三列
        forth_elements_div = soup.find(id='filerDiv').find_all('div')
        if len(forth_elements_div) > 1:
            forth_elements_last_strings = forth_elements_div[0].strings
            mailing_address = ''
            for forth_elements_last_string in forth_elements_last_strings:
                mailing_address = mailing_address + unicode(forth_elements_last_string).encode('utf-8')

            print "mailing_address:",mailing_address.replace("Mailing Address",'')

            forth_elements_second_strings = forth_elements_div[1].strings
            business_address = ''
            for forth_elements_second_string in forth_elements_second_strings:
                business_address = business_address + unicode(forth_elements_second_string).encode('utf-8')

            print "business_address:",business_address.replace('Business Address','')


        #第三栏信息,包含文件信息
        third_tr_elements = soup.find(class_="tableFile").find_all('tr')
        #表格 遍历行
        for i in range(len(third_tr_elements)):
            if i > 0:
                third_tr_td_elements = third_tr_elements[i].find_all('td')
                #遍历列，第三列是文档地址
                if len(third_tr_td_elements) == 5:
                    document_seq = third_tr_td_elements[0].string.encode('utf-8')
                    print "document_seq:",document_seq
                    #print "document_seq type:",type(document_seq)
                    document_description = third_tr_td_elements[1].string.encode('utf-8')
                    print "document_description:",document_description
                    #print "document_description type:",type(document_description)
                    document_url = 'https://www.sec.gov' + third_tr_td_elements[2].find('a')['href'].encode('utf-8')
                    print "document_url:",document_url
                    #print "document_url type:",type(document_url)
                    document_type = third_tr_td_elements[3].string.encode('utf-8')
                    print "document_type:",document_type
                    #print "document_type type:",type(document_type)
                    document_size = third_tr_td_elements[4].string.encode('utf-8')
                    print "document_size:",document_size

    print "+++++++++++++++++++++++++++++++++++++"
    print "#####################################"


def download_file():
    import urllib2
    print "downloading with urllib2"
    url = 'https://www.sec.gov/Archives/edgar/data/1634588/000159140815000004/xslFormDX01/primary_doc.xml'
    url = 'https://www.sec.gov/Archives/edgar/data/1634588/000159140815000004/0001591408-15-000004.txt'
    f = urllib2.urlopen(url)
    data = f.read()
    with open("0001591408-15-000004.txt", "wb") as code:
        code.write(data)

if __name__ == '__main__':
    html = get_html(url)
    get_first_page_info(html)
    # download_file()


