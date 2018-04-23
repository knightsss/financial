__author__ = 'shifx'
import os
# f = open("self_test.pdf",'r')
# lines = f.readlines()
# # print lines
# for i in lines:
#     print i

pwd = os.getcwd()
print pwd
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
print father_path

def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,1)

if __name__ == '__main__':
    la = get_FileSize('self_test2.pdf')
    print la