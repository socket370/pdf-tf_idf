# -*- coding: utf-8 -*-

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

base_path = os.getcwd().replace('\\', '/')
path = base_path + '/data/computer1/'  # 原始数据pdf
path1 = base_path + '/data/ctxt/'  # 处理后的txt
newpath = base_path + '/data/keyword1/'
newpath2 = base_path + '/data/abs/'
newpath3 = base_path + '/data/ref/'


filelist = os.listdir(path)  # 取得当前路径下的所有文件

def get_text():
   for files in filelist:
    filename = os.path.splitext(files)[0]  # 取文件名
    fp = open(path+filename+'.pdf', 'rb')
    #来创建一个pdf文档分析器
    parser = PDFParser(fp)
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr=PDFResourceManager()
        # 设定参数进行分析
        laparams=LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        # 处理每一页
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout=device.get_result()
        for x in layout:
            if(isinstance(x,LTTextBoxHorizontal)):
                with open(path1+filename+'.txt','a+') as f:
                    f.write(x.get_text().encode('utf-8')+'\n')

def get_keyword():
    # getKeyword
    filelist = os.listdir(path1)
    for files in filelist:
        filename = os.path.splitext(files)[0]
        begin = 100000
        end = 10000
        f1 = open(path1 + filename + ".txt", "r")
        f2 = open(newpath + filename + '.txt', "a+")
        for (num, value) in enumerate(f1):
            if value.count("Keywords") > 0:  # 得到关键词的行号
                begin = num
            if num == begin:
                f2.write(value.strip())
                break
        f1.close()
        f2.close()

    filelist = os.listdir(path1)
    for files in filelist:
        filename = os.path.splitext(files)[0]
        begin = 100000
        end = 10000
        f1 = open(path1 + filename + ".txt", "r")
        f2 = open(newpath2 + filename + '.txt', "a+")
        for (num, value) in enumerate(f1):
            if value.count("Abstract") > 0:  # 得到简介的行号
                begin = num
            if value.count("Keywords") > 0:  # 得到关键词的行号
                end = num
            if num > begin and num<end:
                f2.write(value.strip())
        f1.close()
        f2.close()

    '''filelist = os.listdir(path1)
    for files in filelist:
        filename = os.path.splitext(files)[0]
        begin = 100000
        end = 10000
        f1 = open(path1 + filename + ".txt", "r")
        f2 = open(newpath3 + filename + '.txt', "r")
        # lines = len(f1.readlines())
        count = -1
        for index, line in enumerate(f1):
          count += 1
        for (num, value) in enumerate(f1):
            if value.count("References") > 0:  # 得到文献的行号
                begin = num
            if num > begin and num < count:
                f2.write(value.strip())
                f2.write('\n')
        f1.close()
        f2.close()'''




if __name__ == '__main__':
    get_text()
    get_keyword()
    # tfidf_sklearn()