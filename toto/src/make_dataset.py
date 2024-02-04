import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os, re, time

# 웹페이지 주소
toto_url = "https://www.betman.co.kr/main/mainPage/gamebuy/gameSlipIFR.do?gmId=G101&gmTs=210001&gameDivCd=C&isIFR=Y"
data_path = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM\ShowMeTheMoney\toto\data'
driver_path = r'C:\Users\dongh\chromedriver-win64\chromedriver.exe'


def parse_and_format_date(date_string):
    # 정규표현식을 사용하여 월과 일 추출
    match = re.search(r'(\d+\.\d+) \([\w]+\)', date_string)
    
    if match:
        # 월과 일을 '.'을 기준으로 나누기
        month, day = map(int, match.group(1).split('.'))
        
        return month, day

    return None

def parse_to_csv(html, filename):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # 종목
        sport_tag = str(soup.select_one('td span.icoGame'))
        # 정규 표현식을 사용하여 "icoGame small" 다음에 오는 클래스 값과 괄호 안의 내용 추출
        match = re.search(r'<span class="icoGame small (.*?)">([^<]+)</span>', sport_tag)
        sport_tag = match.group(2)

        # 일반 여부
        is_general = "TRUE" if soup.select_one('td span.badge.gray') else "FALSE"

        if sport_tag != "축구" and is_general == 'TRUE':
            # 홈 팀과 점수
            home_team = soup.select_one('.cell.tar span').text
            home_score = get_text(soup, 'div.scoreDiv div.cell.tar strong.score')
            home_score = int(re.search(r'[\d.]+', home_score).group(0))

            # 어웨이 팀과 점수
            away_team = soup.select_one('.cell.tal span:nth-child(2)').text
            away_score = get_text(soup, 'div.scoreDiv div.cell.tal strong.score')
            away_score = int(re.search(r'[\d.]+', away_score).group(0))

            # 배당률
            org_odds = [button.text.strip() for button in soup.select('div.btnChkBox.v2 button span.db')]
            odds = [float(re.search(r'[\d.]+', odd).group(0)) if re.search(r'[\d.]+', odd) else None for odd in org_odds]
            
            # 일자
            date_string = get_text(soup, 'td.fs11', index=1)
            month, day = parse_and_format_date(date_string)

            league = soup.select_one('td span.db.fs11')
            league = league.text.strip() if league else "N/A"

            # 회차
            round_number = soup.select_one('tr[data-matchseq]')['data-matchseq']

            # Winner
            winner = "Home" if home_score > away_score else "Away" if home_score < away_score else "Draw"

            # Bet Type
            bet_type = "UDW" if winner == "Home" and odds[0] < odds[1] else "SUW" if winner == "Home" else "SUW" if odds[0] > odds[1] else "UDW"

            # 데이터 추가
            columns = [round_number, sport_tag, league, home_team, home_score, odds[0], away_team, away_score, odds[1], winner, bet_type, month, day]

            csv_file_path = os.path.join(data_path, f"{filename}.csv")

            # CSV 파일이 존재하지 않는 경우, 헤더를 포함하여 새로 생성
            if not os.path.exists(csv_file_path):
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    
            # 기존 CSV 파일 열기 (데이터 추가 모드)
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)

                # 일반이 TRUE이면 CSV 파일에 데이터 추가
                csv_writer.writerow(columns)

    except Exception as e:
        print(f"에러 발생: {e}")

def get_text(soup, selector, index=0):
    elements = soup.select(selector)
    return elements[index].text.strip() if elements and index < len(elements) else "N/A"

def get_game_info(year, round_num, driver):
    base_url = "https://www.betman.co.kr/main/mainPage/gamebuy/gameSlipIFR.do"
    
    # gmTs 생성
    gmTs = f"{year:02d}{round_num:04d}"
    
    # 파라미터 설정
    params = {
        "gmId": "G101",
        "gmTs": gmTs,
        "gameDivCd": "C",
        "isIFR": "Y"
    }
    
    # URL 조합
    url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    
    # Selenium을 사용하여 웹 페이지 열기
    driver.get(url)

    try:
        # 페이지가 로드될 때까지 기다림
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
        WebDriverWait(driver, timeout=10).until(element_present)
        time.sleep(1)
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 필요한 정보 추출 및 출력
        title = soup.title.text
        print(f"{year}년 {round_num}회차: {title}")

        # HTML 파일로 저장
        with open(f"{data_path}/{year}년_{round_num}회차_total.html", "w", encoding="utf-8") as html_file:
            html_file.write(driver.page_source)

        # tbody 태그의 id가 "tbd_gmBuySlipList"에 해당하는 하위 트리 전체 추출
        target_trees = soup.find_all('tr', {'data-rowindex': lambda x: x and int(x) <= 73})

        # HTML을 문자열로 모아서 파일에 저장
        output_file_name = f"{data_path}\{year}년_{round_num}회차"
        with open(f"{output_file_name}.html", "w", encoding="utf-8") as html_file:
            for index, target_tree in enumerate(target_trees, start=1):
                parse_to_csv(str(target_tree), output_file_name)
            
        # 원하는 정보를 추출하여 반환하거나 처리할 수 있음
        return title
    
    except Exception as e:
        print(f"에러 발생: {e}")
        return None
    
def crawl_betman_info(start_year, start_round, end_year, end_round):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    
    current_year = start_year
    current_round = start_round

    while current_year <= end_year:
        while (current_year < end_year and current_round <= 9999) or (current_year == end_year and current_round <= end_round):
            get_game_info(current_year, current_round, driver)
            current_round += 1

        current_year += 1
        current_round = 1

    # driver.quit()
        
def delete_all_html_files(data_path):
    try:
        # 지정된 디렉토리의 파일 목록 가져오기
        files_in_directory = os.listdir(data_path)

        # HTML 파일만 선택하여 삭제
        html_files = [file for file in files_in_directory if file.endswith(".html")]

        for html_file in html_files:
            file_path = os.path.join(data_path, html_file)
            os.remove(file_path)
            print(f"{file_path} 파일이 삭제되었습니다.")

        print("모든 HTML 파일이 삭제되었습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

# 크롤링 시작
crawl_betman_info(19, 1, 19, 103)
crawl_betman_info(20, 1, 20, 93)
crawl_betman_info(21, 1, 21, 103)
crawl_betman_info(22, 1, 22, 108)
crawl_betman_info(23, 75, 23, 153)
crawl_betman_info(24, 1, 24, 7)
delete_all_html_files(data_path)