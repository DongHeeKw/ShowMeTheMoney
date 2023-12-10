import random
import csv

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
data_path = f'{working_dir}\ShowMeTheMoney\lotto\dataset'

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

def load_frequency_data(file_path):
    frequency_data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            number, frequency = map(int, row)
            frequency_data[number] = frequency
    return frequency_data

def calculate_priority(numbers, frequency_data):
    total_priority = 0
    for num in numbers:
        total_priority += 138 - abs(138 - num)  # Priority based on proximity to 138
        total_priority += frequency_data.get(num, 0)  # Priority based on frequency

    return total_priority

def exec_algo():
    frequency_data = load_frequency_data(f'{data_path}/frequency_num.csv')
    results = []
    for _ in range(100):
        while True:
            generated_numbers = generate_numbers()

            if check_sum_range(generated_numbers):
                break

        priority = calculate_priority(generated_numbers, frequency_data)
        results.append((generated_numbers, priority))

    results.sort(key=lambda x: x[1], reverse=True)  # Sort results based on priority
    selected_result = results[0][0]  # Select the list with the highest priority

    print(selected_result)
    return selected_result