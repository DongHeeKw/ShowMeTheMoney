import smtplib
import subprocess
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read('config.ini')

# 보내는 사람 정보
SENDER_EMAIL = config.get('EMAIL', 'SENDER_EMAIL')
SENDER_PASSWORD = config.get('EMAIL', 'SENDER_PASSWORD')

# 받는 사람 정보
receiver_email = "rhkr9080@gmail.com"   # 받는 사람 이메일 주소

# 이메일 제목
subject = "주간 데이터 분석 결과"

# analyze_data.py 실행 및 결과 얻기
result = subprocess.check_output(["python", "analyze_data.py"], text=True)

# 메일 생성
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = receiver_email
message["Subject"] = subject

# 메일 본문 추가
message.attach(MIMEText(result, "plain"))

# 메일 서버 연결 및 전송
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

print("메일이 성공적으로 전송되었습니다.")
