import random
import csv

working_dir = r'C:\Users\dongh\OneDrive\Desktop\workspace\SMTM'
data_path = f'{working_dir}\ShowMeTheMoney\lotto\dataset'
max_freq_lottonum = 300

def generate_numbers():
    num1 = random.randint(1, 7)
    num2 = random.randint(8, 15)
    num3 = random.randint(16, 23)
    num4 = random.randint(24, 31)
    num5 = random.randint(32, 39)
    num6 = random.randint(40, 45)

    return [num1, num2, num3, num4, num5, num6]

def check_sum_range(numbers):
    total_sum = sum(numbers)
    return 134 <= total_sum <= 142

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
    total_priority_1st = 0.0
    total_priority_2nd = 0.0
    for num in numbers:
        total_priority_1st += 0.8 / (138 - abs(138 - num))  # Priority based on proximity to 138
        total_priority_2nd += 0.0003 * (max_freq_lottonum - frequency_data.get(num, 0))  # Priority based on frequency with lower weight
        
    return total_priority_1st, total_priority_2nd

def exec_algo():
    frequency_data = load_frequency_data(f'{data_path}/frequency_num.csv')
    results = []
    for _ in range(100):
        while True:
            generated_numbers = generate_numbers()
            if check_sum_range(generated_numbers):
                break
        priority_1st, priority_2nd = calculate_priority(generated_numbers, frequency_data)
        print(priority_1st, priority_2nd, priority_1st + priority_2nd)
        results.append((generated_numbers, (priority_1st + priority_2nd)*100))
    results.sort(key=lambda x: x[1], reverse=True)  # Sort results based on priority
    selected_result = results[0][0]  # Select the list with the highest priority

    return selected_result