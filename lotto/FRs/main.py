import exec_algo, exec_random

def main():
    lotto_num_list = []
    algo_iter = 3
    random_iter = 2
    
    # Executing Algorithm
    for _ in range(algo_iter):
        lotto_num_list.append(exec_algo.exec_algo())
    
    # Executing Random
    for _ in range(random_iter):
        lotto_num_list.append(exec_random.exec_random())

    for i, lotto_nums in enumerate(lotto_num_list, start=1):
        print(f'로또 {i} 번호 : {lotto_nums}')

if __name__ == "__main__":
    main()