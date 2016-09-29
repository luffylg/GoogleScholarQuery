import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsReader





class SpiderMain(object):

    def __init__(self,driver):
        self.driver=driver

    def craw(self, mail,names):
        try:
            total_paper=0
            highest_citation=0
            zjuverify(self.driver)
            ele=self.driver.find_element_by_name('q')
            ele.send_keys(mail)
            ele.send_keys(Keys.RETURN)

            zjuverify(self.driver)

            # element = WebDriverWait(driver, 100).until(
            #   EC.presence_of_element_located((By.CLASS_NAME, "button"))
            # )
            # 遍历条目
            rersults=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[@class='gs_r']")
            for j in range(0,len(rersults)):
                # re=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[@class='gs_r']")[j]
                # alist=re.find_elements_by_xpath("/div[@class='gs_ri']/div[@class='gs_a']/a")

                alist=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[{0}]/div[@class='gs_ri']/div[@class='gs_a']/a".format(j+1))
                for i in range(0,len(alist)):
                    a=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[{0}]/div[@class='gs_ri']/div[@class='gs_a']/a".format(j+1))[i]
                    href=a.get_attribute('href')
                    name=a.text.strip()
                    ls=name.split()
                    # 姓名坑，拼接首字母字符串来做不准确的识别
                    # print((names["Firstname"][0]+names["Lastname"][0:2]).lower())
                    # print((ls[0][0]+ls[1][0:2]).lower())
                    if (names["Firstname"][0]+names["Lastname"][0:2]).lower() == (ls[0][0]+ls[1][0:2]).lower():
                        driver.get(href)

                        zjuverify(self.driver)

                        try:
                            total_paper,highest_citation=getnums(driver)
                        except Exception as e:
                            print("getnums method error")
                            driver.back()

                            zjuverify(self.driver)

                            self.driver.find_element_by_name('q').clear()
                            return total_paper, highest_citation
                        driver.back()

                        zjuverify(self.driver)

                        break
                if total_paper!=0 and highest_citation!=0:
                    break
            if total_paper ==0 and highest_citation ==0:
                # 如果找不到个人学术主页，以搜到的结果数为总文章数
                pattern=re.compile(r'\d+')
                st=driver.find_element_by_xpath("//div[@id='gs_ab_md']").text
                total_paper=re.findall(pattern,st)[0]
            # driver.back()
            self.driver.find_element_by_name('q').clear()
        except Exception as e:
            print(e)
            self.driver.find_element_by_name('q').clear()
            return total_paper, highest_citation
        return total_paper, highest_citation
def proxy():
    # 设置代理
    PROXY="127.0.0.1:1085"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    return chrome


def getnums(driver):
    highest_citation=driver.find_element_by_xpath("//tbody[@id='gsc_a_b']/tr[1]/td[@class='gsc_a_c']/a").text

    # 通过判断按钮的disabled属性展开
    while True:
        # print(driver.find_element_by_id('gsc_bpf_more').get_attribute('disabled'))
        if driver.find_element_by_id('gsc_bpf_more').get_attribute('disabled'):
            break
        else:
            # 将页面拖到最底部去点击，否则chrome会发生Element is not clickable at point异常
            driver.execute_script("window.scrollBy(0,200)","")
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")
            time.sleep(1)
            driver.find_element_by_id('gsc_bpf_more').click()
            time.sleep(1)
            # driver.implicitly_wait(10)
    total_paper=driver.find_element_by_id('gsc_a_nn').text.replace(' ','').replace('1–','')
    return total_paper, highest_citation

# 每次发生页面跳转时都要判断需不需要验证
def zjuverify(driver):
    if "浙江大学" in driver.title:
        ele=driver.find_element_by_xpath("//form/input[1]")
        ele.send_keys("心灵之约")
        ele.submit()
        time.sleep(2)

if __name__ == '__main__':
    Namelist=xlsReader.read() # 获取姓名表
    driver=proxy()
    driver.get('https://g.zju.education/extdomains/scholar.google.com/schhp?hl=zh-CN')
    zjuverify(driver)
    # element = WebDriverWait(driver, 100).until(
    #       EC.presence_of_element_located((By.NAME, "q"))
    #     )
    # driver.implicitly_wait(20)
    mail_spider=SpiderMain(driver)
    # 不加encoding可能出现编码错误
    csv=open('res.csv','w',encoding='utf-8')
    for names in Namelist:
        csv=open('res.csv','a',encoding='utf-8')
        mail=names["mail"].strip().split(';')[0]  # 有的邮箱有多个，以分号分隔，取第一个
        total_paper, highest_citation=mail_spider.craw(mail, names)
        names["tital_paper"]=total_paper
        names["highest_citation"]=highest_citation
        print('{0};{1};{2};{3}'.format(names["Firstname"], names["Lastname"], total_paper, highest_citation))
        csv.write('{0};{1};{2};{3}\n'.format(names["Firstname"], names["Lastname"], total_paper, highest_citation))
    csv.close()
    driver.quit()