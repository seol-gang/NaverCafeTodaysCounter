from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import warnings
import ctypes

warnings.filterwarnings("ignore", category=DeprecationWarning)
ctypes.windll.kernel32.SetConsoleTitleW("네이버 카페 오늘자 게시글 및 댓글 카운팅 프로그램 [제작 : blog.naver.com/dev_i_c_e *2차 배포 금지]")

lastCheck = 0
boardCount = 0
replyCount = 0
pageCount = 2

cafeName = input("카페 주소 입력 : ")

driver = webdriver.Chrome('chromedriver')
driver.get('https://nid.naver.com/nidlogin.login')
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#PM_ID_ct > div.header > div.section_navbar > div.area_navigation > ul > li > a > span.an_icon')))

cafeAdress = "https://cafe.naver.com/{0}".format(cafeName)

driver.get(cafeAdress)
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cafe-info-data > ul > li.tit-action > p > a')))
driver.find_element_by_css_selector("#cafe-info-data > ul > li.tit-action > p > a").click()
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ia-action-data > div.ia-info-data3 > ul > li > em > a')))
driver.find_element_by_css_selector("#ia-action-data > div.ia-info-data3 > ul > li > em > a").click()

driver.find_element_by_css_selector("body > div.Flash_det_wrap.activated-detector > span.Flash_det_nosee_area > button > img").click()

iframe = driver.find_element_by_css_selector('#cafe_main')
driver.switch_to_frame(iframe)

iframe = driver.find_element_by_css_selector('#innerNetwork')
driver.switch_to_frame(iframe)



while True:
    data = driver.find_elements_by_css_selector("#main-area > div.article-board.article_profile.m-tcol-c > table > tbody > tr > td.td_date")
    for p in data:
        if p.text.count(':') != 0:
            boardCount += 1
            lastCheck = p.text.count(':')
        else:
            lastCheck = 0

    if lastCheck == 1:
        xpath = "//*[@id=\"main-area\"]/div[3]/a[{0}]".format(pageCount)
        result = driver.find_element_by_xpath(xpath)
        result.click()
        pageCount += 1
        if(pageCount > 11):
            driver.find_element_by_css_selector("#main-area > div.prev-next > a.pgR").click()
            pageCount = 2
            lastCheck = 0
    else:
        driver.switch_to_default_content()
        driver.switch_to_default_content()
        pageCount = 2
        break
        
driver.find_element_by_css_selector("#ia-action-data > div.ia-info-data3 > ul > li.info3 > em > a").click()

iframe = driver.find_element_by_css_selector('#cafe_main')
driver.switch_to_frame(iframe)

iframe = driver.find_element_by_css_selector('#innerNetwork')
driver.switch_to_frame(iframe)

while True:
    data = driver.find_elements_by_css_selector("#main-area > div.article-board.article_profile.m-tcol-c > table > tbody > tr > td.td_date")
    for p in data:
        if p.text.count(':') != 0:
            replyCount += 1
            lastCheck = p.text.count(':')
        else:
            lastCheck = 0
    if lastCheck == 1:
        xpath = "//*[@id=\"main-area\"]/div[3]/a[{0}]".format(pageCount)
        result = driver.find_element_by_xpath(xpath)
        result.click()
        pageCount += 1
        if(pageCount >= 11):
            driver.find_element_by_css_selector("#main-area > div.prev-next > a.pgR").click()
            pageCount = 2
            lastCheck = 0
    else:
        driver.switch_to_default_content()
        driver.switch_to_default_content()
        break

print("오늘 글 쓴 게시물 : {0}개\n오늘 댓글 쓴 갯수 : {1}개".format(boardCount, replyCount))

driver.close()