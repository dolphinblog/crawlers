# coding:utf-8

__author__ = 'CQC'

# 来自http://cuiqingcai.com/993.html，有修改

import urllib
import urllib2
import re
import codecs

# nba
# http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1
# 只看楼主模式下的第一页
# 总结：
# 网页中含有很多不属于ascii编码的字符(所有的汉字、汉字标点符号等等)
# 这些内容作为一个字符串写入到文件对象时
# 该文件对象必须是由f = codecs.open('file.txt', 'a+', 'utf-8')这种方式打开的
# 如果f是由f = open('file.txt', 'a+')得来的，将非ascii字符写入就会报错
# 所有'\n'包括Tools类中的,如果想成功换行，都要改成'\r\n'
class Tools:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\r\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\r\n    ",x)
        x = re.sub(self.replaceBR,"\r\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


class BDTB:
    def __init__(self, baseURL, seeLZ):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tools = Tools()

    def GetPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'返回response这一步出错，错误原因', e.reason
                return None
    def GetPageItems(self, pageCode):
        patternFloors = re.compile('<div.*?j_d_post_content ">(.*?)</div>', re.S)
        findAllResults = re.findall(patternFloors, pageCode) #
        pageFloors = []
        for item in findAllResults:
            content = "\n"+self.tools.replace(item)+"\n"
            pageFloors.append(content)
        return pageFloors
    def WriteInFile(self, pageFloors, page, title, pages, lzCount):
        f = codecs.open('NBA.txt','a','utf-8') ##
        #f=open('NBA.txt', 'a')
        f.write(u'【本帖标题：%s, 共%s页】' % (title, pages))
        f.write('\r\n')
        f.write('\r\n')
        f.write(u'========================================第%s页==============================================' % page)
        f.write('\r\n')
        for floor in pageFloors:
            f.write('\r\n')
            f.write(u'------------------------------------楼主发言楼层-%s------------------------------------' % lzCount)
            f.write('\r\n')           
            f.write('\r\n')
            f.write(floor)
            lzCount += 1
            f.write('\r\n')
        f.write('\r\n')
        f.write('\r\n')
        f.write(u'->第%s页帖子到此结束<-' % page)
        f.write('\r\n')
        f.write('\r\n')
        f.close()
        return lzCount
    def Start(self):
        firstPageCode = self.GetPage(1)
        patternTitle = re.compile('<h3.*?title=.*?>(.*?)</h3>', re.S)
        title = re.search(patternTitle, firstPageCode).group(1)
        patternPages = re.compile('<li class="l_reply_num".*?<span.*?>.*?<span.*?>(.*?)</span>', re.S)
        pages = re.search(patternPages, firstPageCode).group(1)
        pages = int(pages)
        print u'本帖标题为' + title
        print u'在只看楼主模式下，本贴一共有', pages, u'页'
        lzCount = 1
        for page in range(pages):
            print u'现将第%s页写入文档NBA.txt' % (page+1)
            print u'正在获取第%s页所有楼主发言楼层' % (page+1)
            pageCode = self.GetPage(page+1)
            pageItems = self.GetPageItems(pageCode)
            lzCount = self.WriteInFile(pageItems, page+1, title, pages, lzCount)
            print u'第%s页写入完毕' % (page+1)

crawler = BDTB('http://tieba.baidu.com/p/3138733512', 1)
crawler.Start()
