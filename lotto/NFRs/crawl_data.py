import time
import warnings
import requests
from datetime import datetime
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
import os

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
lotto_url = 'https://dhlottery.co.kr'
download_path = r'C:\Users\dongh\Downloads'
downloaded_file = f'{download_path}\excel.xls'
data_path = f'{working_dir}\ShowMeTheMoney\lotto_data'

# warning 메세지 출력 안함
warnings.filterwarnings('ignore')

# 최신 회차 크롤링
def get_max_count():
    url = f'{lotto_url}/common.do?method=main'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    max_count = int(soup.find('strong', id='lottoDrwNo').text)
    print(max_count)
    return(max_count)

# 로또 당첨번호 정보 조회 함수
def crawl_latest_lotto_num(count):
    # url에 회차를 실어 페이지 조회
    url = f'{lotto_url}/gameResult.do?method=byWin&drwNo={count}'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    date = datetime.strptime(soup.find('p', class_='desc').text, '(%Y년 %m월 %d일 추첨)')
    win_number = [int(i) for i in soup.find('div', class_='num win').find('p').text.strip().split('\n')]
    bonus_number = int(soup.find('div', class_='num bonus').find('p').text.strip())
    
    return {
        'date': date, 
        'win_number': win_number, 
        'bonus_number': bonus_number
    }

# 로또 엑셀 데이터 다운로드
def crawl_lotto_exel(param):
    if (param == "All") & (os.path.isfile(f'{data_path}\lotto_raw_data.xls')):
        print("이미 엑셀 파일이 존재합니다.")
        return

    driver_path = r'C:\Users\dongh\chromedriver-win64\chromedriver.exe'

    # Chrome 웹드라이버 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # 브라우저 창 최대화

    # 웹 드라이버 실행
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    # 웹사이트 접속
    url = f'{lotto_url}//gameResult.do?method=byWin'
    driver.get(url)

    if param == "All":
        # 1회차 ~ 최신회차 선택
        dropdown_menu = driver.find_element(By.ID, "drwNoStart")
        select = Select(dropdown_menu)
        select.select_by_visible_text("1")

    # 엑셀 다운로드 버튼 클릭
    excel_button = driver.find_element(By.ID, "exelBtn")
    excel_button.click()     

    # 다운로드가 완료될 때까지 잠시 대기 (시간은 상황에 따라 조절)
    time.sleep(5)

    # 파일이 "Download"폴더에 설치되므로, Working경로로 이동
    if param == "All":
        filename = f'lotto_raw_data.xls'
    elif param == "New":
        filename = f'lotto_raw_data_{datetime.today().strftime("%Y_%m_%d")}.xls'

    import shutil
    shutil.move(downloaded_file, f'{data_path}\{filename}')

    driver.quit()

# crawl_lotto_exel("All")
# crawl_lotto_exel("New")