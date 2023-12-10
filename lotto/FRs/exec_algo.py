import random

def generate_random_number(start, end):
    return random.randint(start, end)

def generate_numbers():
    num1 = generate_random_number(1, 7)
    num2 = generate_random_number(8, 15)
    num3 = generate_random_number(16, 23)
    num4 = generate_random_number(24, 31)
    num5 = generate_random_number(32, 39)
    num6 = generate_random_number(40, 45)

    return [num1, num2, num3, num4, num5, num6]

def check_sum_range(numbers):
    total_sum = sum(numbers)
    return 131 <= total_sum <= 145

def exec_algo():
    while True:
        generated_numbers = generate_numbers()

        if check_sum_range(generated_numbers):
            break
    return generated_numbers
