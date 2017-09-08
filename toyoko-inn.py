# -*- coding: utf-8 -*-
import sys
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chck_in = '20171013'  # 日期
sel_area = '47'  # 區城
sel_htl = '00165'  # 旅館
sel_ldgngPpl = '2'  # 人數
sel_room_clss_Id = '20'  # 房型
sel_room_no = '105921'  # 房名
smoking = '02'  # 吸煙

date = datetime.strptime(chck_in, '%Y%m%d')
year_month = date.strftime('%Y%m')
day = date.strftime('%d').lstrip('0')

driver = webdriver.PhantomJS()
# driver = webdriver.Firefox()
driver.get('https://www.toyoko-inn.com/search')

# 入住日期
datepicker = driver.find_element_by_id('datepicker')
datepicker.click()

for i in range(7):
    datepicker_year = driver.find_element_by_xpath("//span[contains(@class, 'ui-datepicker-year')]").text
    datepicker_month = driver.find_element_by_xpath("//span[contains(@class, 'ui-datepicker-month')]").text
    datepicker_year_month = datepicker_year + re.findall('^\d+', datepicker_month)[0].zfill(2)

    if datepicker_year_month == year_month:
        break
    elif datepicker_year_month < year_month:
        datepicker_next = driver.find_element_by_xpath("//a[contains(@class, 'ui-datepicker-next')]")
        datepicker_next.click()
    else:
        raise Exception('Check-in date less than this month.')

else:
    sys.exit()

datepicker_day = driver.find_element_by_xpath("//table[@class='ui-datepicker-calendar']//a[text()=%s]" % day)
datepicker_day.click()
# 區城
slct_area = driver.find_element_by_id('slct_area')
slct_area_option = slct_area.find_element_by_xpath("//select[@id='slct_area']/option[@value=%s]" % sel_area)
slct_area_option.click()
# 旅館
slct_htl = driver.find_element_by_id('sel_htl')
slct_htl_option = slct_htl.find_element_by_xpath("//select[@id='sel_htl']/option[@value=%s]" % sel_htl)
slct_htl_option.click()
# 人數
slct_ldgngPpl = driver.find_element_by_id('sel_ldgngPpl')
slct_ldgngPpl_option = slct_ldgngPpl.find_element_by_xpath("//select[@id='sel_ldgngPpl']/option[@value=%s]" % sel_ldgngPpl)
slct_ldgngPpl_option.click()
# 禁煙
smokingList_li = driver.find_element_by_xpath("//li[@class='iconTypeSmoke%s']" % smoking)
smokingList_li.click()
# 房型
slct_room_clss_Id = driver.find_element_by_id('sel_room_clss_Id')
slct_room_clss_Id_option = slct_room_clss_Id.find_element_by_xpath("//select[@id='sel_room_clss_Id']/option[@value=%s]" % sel_room_clss_Id)
slct_room_clss_Id_option.click()

# 搜尋
srch_dtl = driver.find_element_by_id('srch_dtl')
srch_dtl.click()

# Page 2
try:
    driver.find_element_by_xpath("//ul[@class='btnLink03']//a[contains(@onclick, %s)]" % sel_room_no)
    message = '查詢結果已可訂房! 請盡速至官網訂購!'
except NoSuchElementException  as e:
    sys.exit()
except Exception as e:
    if hasattr(e, 'message'):
        message = e.message
    else:
        message = e
finally:
    driver.quit()

# 寄送信件
try:
    # 信件內容
    text = MIMEText(message)
    text['Subject'] = 'Toyoko Inn Search Room Service'
    text['From'] = 'service@toyoko-inn.com'
    text['To'] = 'etoanik@gmail.com'
    # 登入伺服器
    server = smtplib.SMTP(host='msa.hinet.net')
    server.sendmail('service@toyoko-inn.com', 'etoanik@gmail.com', text.as_string())
finally:
    server.quit()
