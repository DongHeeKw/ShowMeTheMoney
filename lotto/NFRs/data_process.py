import pandas as pd

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
data_path = f'{working_dir}\ShowMeTheMoney\lotto\dataset'
csv_data_file = f'{data_path}/lotto_data.csv'

# 데이터프레임 생성
df = pd.read_csv(csv_data_file)

# 각 숫자(1부터 6까지의 번호)가 몇 번 나왔는지 세기
num_counts = df.iloc[:, 2:8].values.flatten()
num_counts = pd.Series(num_counts).value_counts()

# 가장 많이 나온 순으로 정렬
sorted_nums = num_counts.sort_values(ascending=False)

# 숫자 합이 가장 많이 나온순으로 정렬
sorted_sums = df['Sum'].value_counts()

# 빈도수가 가장 많은 순으로 정렬된 Series를 새로운 CSV 파일로 저장
sorted_sums.to_csv(f'{data_path}/frequency_sum.csv')