from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsReader


class SpiderMain(object):
    def __init__(self,driver):
        self.driver=driver

    def craw(self, xing, ming):
        # WebDriverWait(driver, 10).until(
        #   EC.presence_of_element_located((By.TAG_NAME, "frameset"))
        #     )
        # self.driver.switch_to.frame(driver.find_element_by_id('content'))
        self.driver.find_element_by_name('CRITERIA_VALUE_1').send_keys(xing)
        Select(self.driver.find_element_by_id('Select13')).select_by_value('AND')
        Select(self.driver.find_element_by_id('CRITERIA_OPTION_2')).select_by_value('FIRSTNAME')
        self.driver.find_element_by_id('CRITERIA_VALUE_2').send_keys(ming)
        self.driver.find_element_by_id('btnSearch').click()
        self.driver.find_element_by_css_selector('#datatable2 tbody ')
        ele=self.driver.find_element_by_xpath("//table[@id='datatable2']/tbody/tr[2]/td[1]/a")
        self.driver.execute_script(ele.get_attribute("href"))
        # 进入详细信息页面
        mail=self.driver.find_element_by_id('email_address').get_attribute('value')
        self.driver.back()
        self.driver.switch_to.frame(driver.find_element_by_id('content'))
        self.driver.find_element_by_id('btnClear').click()
        return mail


def login(driver,username,password):

    driver.get('http://www.editorialmanager.com/zusa/default.aspx')
    # element = WebDriverWait(driver, 100).until(
    #       EC.presence_of_element_located((By.CLASS_NAME, "button"))
    #   )
    # driver.implicitly_wait(10)

    fr=driver.find_element_by_id('content')  # id为content的frame标签
    driver.switch_to.frame(fr)
    driver.implicitly_wait(5)
    ifr=driver.find_element_by_tag_name("iframe")  # 登录的iframe标签
    driver.switch_to.frame(ifr)
    driver.find_element_by_id('username').send_keys(username)  # 用户名
    driver.find_element_by_name('password').send_keys(password)  # 密码
    driver.find_element_by_name('editorLogin').click()
    # 进入选择搜索的界面
    driver.switch_to.frame(driver.find_element_by_id('content'))
    element = WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.LINK_TEXT, "Search People"))
      )
    driver.find_element_by_link_text('Search People').click()
    # 进入search people的页面
    return driver
if __name__ == '__main__':
    username=input('username: ')
    password=input('password: ')
    Namelist=xlsReader.read() # 获取姓名表
    driver=webdriver.Chrome()
    login(driver,username,password)
    mail_spider=SpiderMain(driver)
    for names in Namelist:
        ming=names["Firstname"].strip()
        xing=names["Lastname"].strip()
        mail=mail_spider.craw(xing,ming)
        print(mail)


