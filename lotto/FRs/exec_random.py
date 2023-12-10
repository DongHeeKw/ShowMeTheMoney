import random

def generate_lotto_numbers():
    # 1부터 45까지의 숫자 중에서 6개를 선택
    lotto_numbers = random.sample(range(1, 46), 6)
    return sorted(lotto_numbers)

def generate_multi_lotto_numbers(num_tickets):
    # num_tickets 개수만큼 로또 번호 생성하여 리스트로 변환
    return [generate_lotto_numbers() for _ in range(num_tickets)]

def exec_random():
    list_lotto_numbers = generate_lotto_numbers()
    return list_lotto_numbers

