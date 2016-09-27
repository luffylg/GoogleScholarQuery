import re
import requests
from bs4 import BeautifulSoup

import html_parser

import xlsReader

# 读取excel文件批量寻找邮箱
class SpiderMain(object):
    def __init__(self,xing,ming):
        self.parser = html_parser.HtmlParser()
        self.xing=xing
        self.ming=ming
        self.param={'origin':'searchauthorlookup',
                   'src':'al',
                   'edit':'',
                   'poppUp':'',
                   'basicTab':'',
                   'affiliationTab':'',
                   'advancedTab':'',
                   'st1':xing,
                   'st2':ming,
                   'institute':'',
                   '_exactSearch':'on',
                   'orcidId':'',
                   #'authSubject':'LFSC',
                   '_authSubject':'on',
                   #'authSubject':'HLSC',
                    '_authSubject':'on',
                    #'authSubject':'PHSC',
                    '_authSubject':'on',
                    #'authSubject':'SOSC',
                    '_authSubject':'on',
                    's':'AUTH--LAST--NAME({0}) AND AUTH--FIRST({1})'.format(ming,xing),
                    'sdt':'al',
                    'sot':'al',
                    #'searchId':sid,
                    #'sid':sid
                   }

    def craw(self):
        try:
            root='https://www.scopus.com/results/authorNamesList.uri'
            ses=requests.session()#创建session
            #ses.proxies={'https':'http://127.0.0.1:1085'}#代理
            s=ses.get(root,params=self.param)#搜索得到作者列表页面
            AuthorID=self.parser.GetAuthorId(s)#获取authorid
            if(AuthorID==False):
                return "no mail"

            else:
                return self.crawel(ses,AuthorID)
        except:
            return "error"

    def crawel(self,ses, AuthorID,bianhao=0):
        s2=ses.get('https://www.scopus.com/authid/detail.uri',params={'authorId':AuthorID})# 获取作者详细信息页面
        message=self.parser.GetAuthorMessage(s2)#获取详细信息
        wenxin=message[0]
        AuthorName=message[1]
        area=message[2]
        lishi=message[4]
        # print('文献数：'+wenxin+' '+lishi)
        # print(AuthorName)
        # print(area)
        Articlelink=message[3]#获取作者所有文章页面链接
        s3=ses.get(Articlelink)#获取作者所有文章页面
        Articles=self.parser.GetArticles(s3)#获得所有文章链接及年份列表
        for lists in Articles:
            link=lists[0]
            nian=lists[1]
            s4=ses.get(link)#获取文章详细信息页面
            emailnotparse,suoxie=self.parser.GetEmail(s4)#得到加密的邮件地址
            if emailnotparse!=None:
                if bianhao!=0:
                    print('第'+str(bianhao)+'作者')
                email=strip_email_protection(emailnotparse['href'])
                #print('<a href=\''+email+'\'>'+email+'></a>')
                return email
        return "no mail"
        #print("没找到邮箱")




def strip_email_protection(s):
    #解密邮件地址
    fp = re.findall(r'email-protection#[A-Za-z0-9]+', s)
    #parse email
    fp = fp[0].replace('email-protection#','')
    # print(fp)
    r = int(fp[:2], 16)
    email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
    # m = re.sub(r'<a class="__cf_email__".*?</a>', email, s)
    # #strip <script>
    # m = re.sub('<script.*?</script>', '', s, flags = re.DOTALL)
    return email



if __name__=="__main__":
    Namelist=xlsReader.read() # 获取姓名表
    for names in Namelist:
        ming=names["Firstname"].strip()
        xing=names["Lastname"].strip()
        obj_spider=SpiderMain(xing,ming)
        mail=obj_spider.craw()
        print(mail)

