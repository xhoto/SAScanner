import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sa_config as sc

# download chromedriver https://sites.google.com/a/chromium.org/chromedriver/home
driver = webdriver.Chrome() 
wait = WebDriverWait(driver, 10)

# open main url
driver.get(sc.main_url)
time.sleep(2)

# find login url in main page
# "action_logging_common('TOP_03'); cms.goToLink('/I/KR/KO/viewLogin.do?callType=IBE&menuId=CM201802220000728453');"
login_url = driver.find_element_by_link_text('로그인').get_attribute('onclick')
login_url = login_url.replace("action_logging_common('TOP_03'); cms.goToLink('","")
login_url = sc.main_url + login_url.replace("');","")

# open login page
driver.get(login_url)
time.sleep(5)

userid = driver.find_element_by_id('txtID')
userid.send_keys(sc.login_ID)
time.sleep(1)

password = driver.find_element_by_id('txtPW')
password.send_keys(sc.login_PW)
time.sleep(1)


loginbtn = driver.find_element_by_id('btnLogin')
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(loginbtn).click().perform()
time.sleep(5)

# open star alliance search page
driver.get(sc.search_url)
time.sleep(5)

# 출발공항 선택
btnDepartureAirport = driver.find_element_by_xpath("//div[@class='itinerary_select spot_proven']/a")
departureAirportAction = webdriver.ActionChains(driver)
departureAirportAction.move_to_element(btnDepartureAirport).click().perform()
time.sleep(5)

txtAirport = driver.find_element_by_xpath("//div[@class='flights_list star_air']/input")
txtAirport.send_keys('ICN')

bbb = driver.find_element_by_xpath("//div[@class='flights_list star_air']/button")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(bbb).click().perform()
time.sleep(1)

btnSelectedAirport = driver.find_element_by_xpath("//li[@airport='ICN']/a")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnSelectedAirport).click().perform()
time.sleep(1)

# 도착공항 선택
btnArrivalAirport = driver.find_element_by_xpath("//div[@class='itinerary_select spot_destin']/a")
arrivalAirportAction = webdriver.ActionChains(driver)
arrivalAirportAction.move_to_element(btnArrivalAirport).click().perform()
time.sleep(5)

txtAirport = driver.find_element_by_xpath("//div[@class='flights_list star_air']/input")
txtAirport.send_keys('FRA')

bbb = driver.find_element_by_xpath("//div[@class='flights_list star_air']/button")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(bbb).click().perform()
time.sleep(1)

btnSelectedAirport = driver.find_element_by_xpath("//li[@airport='FRA']/a")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnSelectedAirport).click().perform()
time.sleep(1)

###########################
# 날짜선택
# hiddenDepartureDate = driver.find_element_by_xpath("//input[@id='departureDate']")
# hiddenDepartureDate.setAttribute("value", "20200306")

## TODO 날짜 선택
# btn_coupon_layer
btnCal = driver.find_element_by_id("sCalendar1")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnCal).click().perform()
time.sleep(1)

#######################

# 성인
txtAdultCount = driver.find_element_by_id("adultCount")
txtAdultCount.send_keys('1')

# 소아
txtChildCount = driver.find_element_by_id("childCount")
txtChildCount.send_keys('0')

# class
btnClass = driver.find_element_by_xpath("//a[@name='cabinClassAll']")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnClass).click().perform()

# btn_coupon_layer
btnCL = driver.find_element_by_id("btn_coupon_layer")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnCL).click().perform()
time.sleep(1)

# btn_M red
btnSS = driver.find_element_by_xpath("//button[@class='btn_M red']")
mouse = webdriver.ActionChains(driver)
mouse.move_to_element(btnSS).click().perform()

print ('test')