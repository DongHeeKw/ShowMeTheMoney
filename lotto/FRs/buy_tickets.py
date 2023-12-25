from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser

# 경로 설정 (ChromeDriver 등)
working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
lotto_url = 'https://dhlottery.co.kr'
driver_path = r'C:\Users\dongh\chromedriver-win64\chromedriver.exe'

def login():
    # 웹사이트 접속
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(f'{lotto_url}/common.do?method=main')


    # 설정 파일 읽기
    config = configparser.ConfigParser()
    config.read(f'{working_dir}\ShowMeTheMoney\config.ini')

    # 사용자 정보 가져오기
    username = config['Credentials']['username']
    password = config['Credentials']['password']

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.CSS_SELECTOR, 'a.btn_common.sml[href*="/user.do?method=login"]')
    driver.execute_script("arguments[0].click();", login_button)

    # 페이지 로드가 완료될 때까지 대기 (최대 10초)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "userId"))
    )
    # 아이디와 패스워드 입력
    id_input = driver.find_element(By.NAME, "userId")
    id_input.send_keys(username)

    pw_input = driver.find_element(By.NAME, "password")
    pw_input.send_keys(password)

    login_button = driver.find_element(By.CLASS_NAME, 'btn_common.lrg.blu')
    driver.execute_script("arguments[0].click();", login_button)

    # "구매하기" 버튼 클릭
    # 페이지 로드가 완료될 때까지 대기 (최대 10초)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId")))
    buy_button = driver.find_element(By.CSS_SELECTOR, 'a.btn_common.smid.gblu[href="/gameInfo.do?method=buyLotto&amp;wiselog=C_A_1_3"]')
    driver.execute_script("arguments[0].click();", buy_button)

    driver.quit()

login()