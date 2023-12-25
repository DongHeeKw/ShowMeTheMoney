from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# 웹페이지 주소
toto_url = "https://www.betman.co.kr/main/mainPage/gamebuy/gameSlipIFR.do?gmId=G101&gmTs=210001&gameDivCd=C&isIFR=Y"
driver_path = r'C:\Users\dongh\chromedriver-win64\chromedriver.exe'

def extract_year_and_round(option_value):
    # 정규표현식을 사용하여 숫자만 추출
    match = re.search(r'(\d+)(\d{3})', option_value)
    if match:
        year = match.group(1)
        round_number = match.group(2)
        return year, round_number
    return None, None

def select_round(driver, round_number):
    driver.get(toto_url)

    # 드롭다운 요소 찾기
    dropdown = driver.find_element("id", "selectBoxGameRnd")

    # 드롭다운 선택을 위한 Select 객체 생성
    select = Select(dropdown)

    # 드롭다운의 모든 옵션 값 가져오기
    all_options = [option.get_attribute("value") for option in select.options]
    print(all_options)

    # # 회차 선택
    # option_value = f"G101,{round_number:06d}"  # 회차 번호 형식에 맞춰서 생성
    # print(option_value)
    
    # 21년부터 23년까지의 회차만 선택
    for year in range(21, 24):
        for round_num in range(1, round_number + 1):
            option_value = f"G101,{year:02d}{round_num:04d}"  # 회차 번호 형식에 맞춰서 생성
            select.select_by_value(option_value)

            print(option_value)

            # 버튼 클릭
            search_button = driver.find_element(By.ID, "btnSearchSlip")
            search_button.click()

            # # 페이지 로딩을 위해 충분한 시간 기다리기 (원하는 조건으로 변경 가능)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "some_element_on_the_next_page")))

                        # 선택된 회차의 HTML 가져오기
            try:
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 년도와 회차 추출
                extracted_year, extracted_round = extract_year_and_round(option_value)

                # 여기에 원하는 동작 수행
                print(f"현재 {extracted_year}년 {extracted_round}회차의 HTML:\n{html}")

            except StaleElementReferenceException:
                print(f"StaleElementReferenceException occurred. Retrying...")

driver = webdriver.Chrome(executable_path=driver_path)

# 선택하고 싶은 회차
for round_number in range(1, 151):
    # 함수 호출
    select_round(driver, round_number)