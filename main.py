import os
import sys
import time
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv

asianaUrl = 'https://www.flyasiana.com'
searchUrl = 'https://www.flyasiana.com/I/KR/KO/RedemptionStarAllianceRegistTravel.do'

def loadConfig():
    # TODO: xhoto.choi 20200215 json 에서 가지고 오도록
    loginID = ''
    loginPW = ''
    departureAirportCode = 'FRA'
    arrivalAirportCode = 'ICN'
    adultCount = 3
    classE = False
    classB = True

    return loginID, loginPW, departureAirportCode, arrivalAirportCode, adultCount, classE, classB

# TODO: xhoto.choi 20200215 손봐야됨.
def ExportCSV(scheduleList):
    try:
        with open('test.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            scheduleList.insert(0, ['Date','From','To','Depature', 'FlyingTime', 'Arrival', 'Flight', 'Aircraft', 'AvailableSeat'])
            wr.writerow(scheduleList)
    except IOError:
        print("I/O error")

def SelectDate(searchDate):

    # TODO: xhoto.choi 20200221 날짜 체크 현재보다 3일뒤부터 조회가능
    dMonth = searchDate.month
    dYear = searchDate.year
    dDay = searchDate.day

    btnOpenCalendar = driver.find_element_by_id("sCalendar1")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnOpenCalendar).click().perform()

    moveStep = 0
    monthOfToday = date.today().month

    if monthOfToday > dMonth:
        moveStep = 9 + (monthOfToday - dMonth)  
    elif monthOfToday == dMonth or monthOfToday == dMonth + 1:
        moveStep = 0
    else:
        moveStep = dMonth - (monthOfToday+1) 

    for i in range(0, moveStep):
        btnNextMonth = driver.find_element_by_xpath("//a[@data-handler='next'][@title='다음달']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnNextMonth).click().perform()
        time.sleep(0.2)

    btnSelectedDay = driver.find_element_by_xpath("//td[@data-month='" + str(dMonth - 1) + "'][@data-year='" + str(dYear) + "']//a[@class='ui-state-default'][text()='" + str(dDay) + "']")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnSelectedDay).click().perform()

def SelectAirport(xpathAirportSearch, airportCode):
    btnAirportSearch = driver.find_element_by_xpath(xpathAirportSearch)
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnAirportSearch).click().perform()
    time.sleep(0.2)

    txtAirport = driver.find_element_by_xpath("//div[@class='flights_list star_air']/input")
    txtAirport.send_keys(airportCode)

    btnSelectAirport = driver.find_element_by_xpath("//div[@class='flights_list star_air']/button")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnSelectAirport).click().perform()
    time.sleep(0.2)

    btnUseSelectedAirpot = driver.find_element_by_xpath("//li[@airport='" + airportCode + "']/a")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnUseSelectedAirpot).click().perform()
    time.sleep(0.2)

def SelectPassenger(adultCount):
    txtAdultCount = driver.find_element_by_id("adultCount") # (성인만 선택, 소아/유아는 전화로 예약해야됨)
    txtAdultCount.send_keys(adultCount)

def SelectCabinClass(classE, classB):
    if classE:
        btnClassE = driver.find_element_by_xpath("//a[@cabinclass='E']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnClassE).click().perform()

    if classB:
        btnClassB = driver.find_element_by_xpath("//a[@cabinclass='B']")
        mouse = webdriver.ActionChains(driver)
        mouse.move_to_element(btnClassB).click().perform()

def login(id, pwd):
    driver.get(asianaUrl)
    time.sleep(2)

    loginUrl = driver.find_element_by_link_text('로그인').get_attribute('onclick')
    loginUrl = loginUrl.replace("action_logging_common('TOP_03'); cms.goToLink('","")
    loginUrl = asianaUrl + loginUrl.replace("');","")    
    driver.get(loginUrl)

    userid = driver.find_element_by_id('txtID')
    userid.send_keys(id)
    password = driver.find_element_by_id('txtPW')
    password.send_keys(pwd)
    loginbtn = driver.find_element_by_id('btnLogin')
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(loginbtn).click().perform()
    time.sleep(2)

    # TODO: xhoto.choi 2020015 로그인 실패 예외처리

def Search(dAirportCode, aAirportCode, searchDate, adultCount=3, classE=True, classB=True):
    driver.get(searchUrl)
    time.sleep(2)

    SelectAirport("//div[@class='itinerary_select spot_proven']/a", dAirportCode)
    SelectAirport("//div[@class='itinerary_select spot_destin']/a", aAirportCode)
    SelectDate(searchDate)
    SelectPassenger(adultCount)
    SelectCabinClass(classE, classB)

    btnCL = driver.find_element_by_id("btn_coupon_layer")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnCL).click().perform()
    time.sleep(2)

    btnSS = driver.find_element_by_xpath("//button[text()='예매 진행']")
    mouse = webdriver.ActionChains(driver)
    mouse.move_to_element(btnSS).click().perform()

    time.sleep(20)

    flights = driver.find_elements_by_xpath("//tr[@class='flight'][@layover='false']")
    if len(flights) != 0:
        for flight in flights:
            flight = flight.text \
                .replace('\n루프트한자 독일 항공 운항', '') \
                .replace('\n운항', '') \
                .replace('시간',':') \
                .replace('분','') \
                .replace('\n직항','') \
                .replace('석','') \
                .replace('+1DAY\n','+') \
                .replace('\n','\t')
            flight = searchDate.strftime("%Y-%m-%d") + ' ' + (searchDate.strftime('%A'))[:3] + '\t' + dAirportCode + '\t' + aAirportCode + '\t' + flight
            # TODO: xhoto.choi 20200221 pandas 나 list 써서 export to json or csv
            print(flight)  
    time.sleep(1)

def SearchRange(departureAirport, arrivalAirport, startDate, endDate, adultCount, classE=True, classB=True):
    deltaDate = endDate - startDate
    for i in range(deltaDate.days + 1):
        searchDate = startDate + timedelta(days=i)
        Search(departureAirport, arrivalAirport, searchDate, adultCount, classE, classB)
    # ExportCSV(finalScheduleList)

def main():
    loginID, loginPW, departureAirportCode, arrivalAirportCode, adultCount, classE, classB = loadConfig()
    login(loginID, loginPW)
    print ('\t'.join(['일자\t','출발','도착','출발', '비행', '도착', '편명', '기체', '좌석']))
    SearchRange(departureAirportCode, arrivalAirportCode, date(2020,4,2), date(2020,4, 3), adultCount, classE, classB)

if __name__ == "__main__":    
    # download chromedriver https://sites.google.com/a/chromium.org/chromedriver/home
    driver = webdriver.Chrome() 
    wait = WebDriverWait(driver, 10)
    main()
    driver.close()