from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import configparser

# 설정 파일 읽기
config = configparser.ConfigParser()
config.read('config.ini')

# 사용자 정보 가져오기
username = config['Credentials']['username']
password = config['Credentials']['password']

# 웹드라이버 경로 설정 (ChromeDriver 등)
driver_path = '/path/to/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)