import pandas as pd
from datetime import datetime

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
data_path = f'{working_dir}\ShowMeTheMoney\data'

def convert_xls_to_xlsx(input_path, output_path):
    # xls 파일을 DataFrame으로 읽기
    df = pd.read_excel(input_path, engine='xlrd')

    # DataFrame을 xlsx 파일로 저장
    df.to_excel(output_path, index=False, engine='openpyxl')

    print(f"{input_path} 파일이 성공적으로 {output_path} 파일로 변환되었습니다.")

def convert_exel_to_csv(exel_file_path, csv_file_path):
    # 엑셀 파일을 DataFrame으로 읽기
    df = pd.read_excel(exel_file_path)

    # DataFrame을 CSV 파일로 저장
    df.to_csv(csv_file_path, index = False)

    print(f"{exel_file_path} 파일이 성적공으로 {csv_file_path} 파일로 변환되었습니다.")

def process_raw_csv(input_path, output_path):
    df = pd.read_csv(input_path)
    
    #필요한 열만 선택
    selected_columns = ['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 13','Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19']
    df_selected = df[selected_columns]

    # 열 이름 변경
    df_selected.columns = ['Round', 'Date', '1stNum', '2ndNum', '3rdNum', '4thNum', '5thNum', '6thNum', 'BonusNum']

    # '회차' 기준으로 정렬
    df_selected.drop(df.index[0:2], inplace=True)
    df_selected = df_selected.ffill().sort_values('Date')
    
    # 로또번호 정수형으로 변경
    df_selected['1stNum'] = df_selected['1stNum'].astype(int)
    df_selected['2ndNum'] = df_selected['2ndNum'].astype(int)
    df_selected['3rdNum'] = df_selected['3rdNum'].astype(int)
    df_selected['4thNum'] = df_selected['4thNum'].astype(int)
    df_selected['5thNum'] = df_selected['5thNum'].astype(int)
    df_selected['6thNum'] = df_selected['6thNum'].astype(int)
    df_selected['BonusNum'] = df_selected['BonusNum'].astype(int)

    df_selected['Sum'] = df_selected.iloc[:, 2:8].sum(axis=1)

    new_csv_file_path = output_path

    # 데이터프레임을 새로운 CSV 파일로 저장
    df_selected.to_csv(new_csv_file_path, index=False)

    print(f"데이터프레임이 {new_csv_file_path} 파일로 성공적으로 저장되었습니다.")

process_raw_csv(f'{data_path}/lotto_raw_data.csv', f'{data_path}/lotto_data.csv')
