import random

def generate_lotto_numbers():
    # 1부터 45까지의 숫자 중에서 6개를 선택
    lotto_numbers = random.sample(range(1, 46), 6)
    return sorted(lotto_numbers)

def generate_multi_lotto_numbers(num_tickets):
    # num_tickets 개수만큼 로또 번호 생성하여 리스트로 변환
    return [generate_lotto_numbers() for _ in range(num_tickets)]


# 5000원 어치 구매!
num_tickets = 5
list_lotto_numbers = generate_multi_lotto_numbers(5)

for i, lotto_numbers in enumerate(list_lotto_numbers, start = 1):
    print(f"로또 {i} 번호", lotto_numbers)