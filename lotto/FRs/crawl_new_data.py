# 이미 csv dataset이 구축되었다고 가정
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pandas as pd

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
lotto_url = 'https://dhlottery.co.kr'
data_path = f'{working_dir}\ShowMeTheMoney\lotto\data'

# 최신 회차 크롤링
def get_max_count():
    url = f'{lotto_url}/common.do?method=main'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    max_count = int(soup.find('strong', id='lottoDrwNo').text)
    return(max_count)


# 로또 당첨번호 정보 조회 함수
def crawl_latest_lotto_num(count):
    # url에 회차를 실어 페이지 조회
    url = f'{lotto_url}/gameResult.do?method=byWin&drwNo={count}'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    round = get_max_count()
    date = datetime.strptime(soup.find('p', class_='desc').text, '(%Y년 %m월 %d일 추첨)').strftime('%Y.%m.%d')
    win_number = [int(i) for i in soup.find('div', class_='num win').find('p').text.strip().split('\n')]
    bonus_number = int(soup.find('div', class_='num bonus').find('p').text.strip())
    sum_number = 0
    for i in win_number:
        sum_number += i
    
    return {
        'Round' : round,
        'Date': date, 
        '1stNum': win_number[0],
        '2ndNum': win_number[1],
        '3rdNum': win_number[2],
        '4thNum': win_number[3],
        '5thNum': win_number[4],
        '6thNum': win_number[5],
        'BonusNum': bonus_number,
        'Sum' : sum_number
    }

def update_new_data():
    new_data = crawl_latest_lotto_num(get_max_count())
    csv_data_file = f'{data_path}/lotto_data.csv'
    
    # 기존 CSV 파일 불러오기
    df_existing = pd.read_csv(csv_data_file)

    if new_data['Round'] in df_existing['Round'].values:
        print("이미 존재하는 회차입니다. 데이터 업데이트를 수행하지 않습니다.")
        return

    # 새로운 데이터를 DataFrame으로 변환
    df_new = pd.DataFrame([new_data])

    print(df_new)

    # 기존 데이터프레임과 새로운 데이터프레임을 합치기
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    
    # 업데이트된 데이터를 CSV 파일로 저장
    df_combined.to_csv(csv_data_file, index=False)

    print("데이터가 성공적으로 업데이트되었습니다.")

update_new_data()