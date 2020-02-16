import os
import sys
import time
from datetime import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sa_config as sc

def SelectDate(dYear, dMonth, dDay):
    # 날짜선택
    btnCal = driver.find_element_by_id("sCalendar1")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnCal).click().perform()

    moveStep = 0
    monthOfToday = date.today().month

    if monthOfToday > dMonth: # 2 1 > 10번 # 4 2 > 8번
        moveStep = 9 + (monthOfToday - dMonth)
    elif monthOfToday == dMonth or monthOfToday == dMonth + 1:
        moveStep = 0
    else:
        moveStep = dMonth - (monthOfToday+1) 

    for i in range(0, moveStep):
        btnNextMonth = driver.find_element_by_xpath("//a[@data-handler='next'][@title='다음달']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnNextMonth).click().perform()
        time.sleep(0.5)

    btnDay4 = driver.find_element_by_xpath("//td[@data-month='" + str(dMonth - 1) + "'][@data-year='" + str(dYear) + "']//a[@class='ui-state-default'][text()='" + str(dDay) + "']")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnDay4).click().perform()

def SelectAirport(xpathAirportSearch, airportCode):

    btnAirportSearch = driver.find_element_by_xpath(xpathAirportSearch)
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnAirportSearch).click().perform()
    time.sleep(0.5)

    txtAirport = driver.find_element_by_xpath("//div[@class='flights_list star_air']/input")
    txtAirport.send_keys(airportCode)

    btnAirportSearch2 = driver.find_element_by_xpath("//div[@class='flights_list star_air']/button")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnAirportSearch2).click().perform()
    time.sleep(0.5)

    btnSelectedAirport = driver.find_element_by_xpath("//li[@airport='" + airportCode + "']/a")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnSelectedAirport).click().perform()
    time.sleep(0.5)

def Search(dAirportCode, aAirportCode, dYear, dMonth, dDay, classE=True, classB=True, adultCount=3):
    
    # open star alliance search page
    driver.get(sc.search_url)
    time.sleep(2)

    # 출발공항
    SelectAirport("//div[@class='itinerary_select spot_proven']/a", dAirportCode)
    # 도착공항
    SelectAirport("//div[@class='itinerary_select spot_destin']/a", aAirportCode)
    # 날짜
    SelectDate(dYear, dMonth, dDay)

    # 탑승인원 (성인만 선택, 소아/유아는 전화로 예약해야됨)
    txtAdultCount = driver.find_element_by_id("adultCount")
    txtAdultCount.send_keys(adultCount)

    # 좌석등급
    if classE:
        btnClassE = driver.find_element_by_xpath("//a[@cabinclass='E']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnClassE).click().perform()

    if classB:
        btnClassB = driver.find_element_by_xpath("//a[@cabinclass='B']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnClassB).click().perform()

    # 검색
    btnCL = driver.find_element_by_id("btn_coupon_layer")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnCL).click().perform()
    time.sleep(2)

    btnSS = driver.find_element_by_xpath("//button[text()='예매 진행']")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnSS).click().perform()

    time.sleep(20)

    dDate = datetime(year=dYear, month=dMonth, day=dDay)

    # 검색 결과 출력
    flights = driver.find_elements_by_xpath("//tr[@class='flight'][@layover='false']")
    if len(flights) == 0:
        print(dDate.strftime("%Y-%m-%d") + '\t' + dAirportCode + '\t' + aAirportCode + '\tnone')
    else:
        for flight in flights:
            flight = flight.text \
                .replace('\n루프트한자 독일 항공 운항', '') \
                .replace('\n운항', '') \
                .replace('시간',':') \
                .replace('분','') \
                .replace('직항','0') \
                .replace('석','') \
                .replace('\n+1Day','+1 ') \
                .replace('\n','\t')
            print(dDate.strftime("%Y-%m-%d") + ' ' + (dDate.strftime('%A'))[:3] + '\t' + dAirportCode + '\t' + aAirportCode + '\t' + flight)
    
    time.sleep(5)

def SearchRange(dAirportCode, aAirportCode, startMonth, endMonth, classE=True, classB=True):
    daysInMonth = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for m in range(startMonth, endMonth+1):
        for d in range(1, daysInMonth[m]):
            Search(dAirportCode, aAirportCode, 2020, m, d, classE, classB)

def main():
    a1 = sys.argv[1]
    a2 = sys.argv[2]

    # download chromedriver https://sites.google.com/a/chromium.org/chromedriver/home

    wait = WebDriverWait(driver, 10)

    # 아시아나 접속
    driver.get(sc.main_url)
    time.sleep(2)

    # 로그인페이지 이동
    login_url = driver.find_element_by_link_text('로그인').get_attribute('onclick')
    login_url = login_url.replace("action_logging_common('TOP_03'); cms.goToLink('","")
    login_url = sc.main_url + login_url.replace("');","")
    driver.get(login_url)

    #로그인
    userid = driver.find_element_by_id('txtID')
    userid.send_keys(sc.login_ID)
    password = driver.find_element_by_id('txtPW')
    password.send_keys(sc.login_PW)
    loginbtn = driver.find_element_by_id('btnLogin')
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(loginbtn).click().perform()
    time.sleep(2)

    classE = False
    classB = True

    if classE and classB:
        print('날짜\t\t출발\t도착\t출발T\t비행\t경유\t도착T\t편명\t기종\tEco\tBiz')
    elif classE:
        print('날짜\t\t출발\t도착\t출발T\t비행\t경유\t도착T\t편명\t기종\tEco')
    elif classB:
        print('날짜\t\t출발\t도착\t출발T\t비행\t경유\t도착T\t편명\t기종\tBiz')

    SearchRange(a1, a2, 7, 7, classE, classB)
    SearchRange(a2, a1, 7, 7, classE, classB)

if __name__ == "__main__":
    driver = webdriver.Chrome() 
    main()

driver.close()