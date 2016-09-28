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
            tital_paper=0
            highest_citation=0
            ele=self.driver.find_element_by_name('q')
            ele.send_keys(mail)
            ele.send_keys(Keys.RETURN)

            # element = WebDriverWait(driver, 100).until(
            #   EC.presence_of_element_located((By.CLASS_NAME, "button"))
            # )
            alist=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[1]/div/div[@class='gs_a']/a")
            for i in range(0,len(alist)):
                a=self.driver.find_elements_by_xpath("//div[@id='gs_ccl_results']/div[1]/div/div[@class='gs_a']/a")[i]
                href=a.get_attribute('href')
                name=a.text.strip()
                ls=name.split()
                # 姓名坑，拼接首字母字符串来做不准确的识别
                # print((names["Firstname"][0]+names["Lastname"][0:2]).lower())
                # print((ls[0][0]+ls[1][0:2]).lower())
                if (names["Firstname"][0]+names["Lastname"][0:2]).lower() == (ls[0][0]+ls[1][0:2]).lower():
                    driver.get(href)
                    tital_paper,highest_citation=getnums(driver)
                    driver.back()
                    break
            # driver.back()
            self.driver.find_element_by_name('q').clear()
        except:
            return tital_paper, highest_citation
        return tital_paper, highest_citation
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
    tital_paper=driver.find_element_by_id('gsc_a_nn').text.replace(' ','').replace('1–','')
    return tital_paper, highest_citation

if __name__ == '__main__':
    Namelist=xlsReader.read() # 获取姓名表
    driver=proxy()
    driver.get('https://g.zju.education/extdomains/scholar.google.com/schhp?hl=zh-CN')
    # element = WebDriverWait(driver, 100).until(
    #       EC.presence_of_element_located((By.NAME, "q"))
    #     )
    # driver.implicitly_wait(20)
    mail_spider=SpiderMain(driver)
    for names in Namelist:
        mail=names["mail"].strip().split(';')[0]  # 有的邮箱有多个，以分号分隔，取第一个
        tital_paper, highest_citation=mail_spider.craw(mail,names)
        names["tital_paper"]=tital_paper
        names["highest_citation"]=highest_citation
        print('{0};{1};{2};'.format(names["Firstname"],names["Lastname"],tital_paper,highest_citation))

    # driver.quit()