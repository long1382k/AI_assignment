import sys

import numpy as np
import itertools
import random
import logging


# first column is value second is weight of each item

POPULATION = 10 # Số các tập mẫu khởi tạo
THRESHOLD = 0.5
MUTATION = 0.1
CHANGE_PER_ITER = 150
LIMIT_ITERATION = 1000
PRINT_PER_IT = 20

class knapsack_population:
    def __init__(self):
        population = []

    def create_population(self, data, max_weight, num):
        """Creation of population that is legal"""
        #data: số cặp v,w mảng 2 chiều
        population = []
        for i in range(num): #num: số lượng các bộ chrmosome
            total_value = 0 # Tổng giá trị
            total_weight = 0 # Tổng khối lượng
            chromosome = [0] * len(data) # Tạo mảng full 0 độ dài = số cặp v,w
            for j in range(len(data)):
                if random.uniform(0, 1) > THRESHOLD and total_weight < max_weight: # Xác suất đủ lớn, tổng KL < W ????
                    chromosome[j] = 1
                    total_value += data[j, 0]
                    total_weight += data[j, 1]
            population.append(chromosome) # Thêm bộ NST
        return population
    def fitness(self, my_data, population, chromosome):
        """calculation of score and sort"""
        d = {} # có dạng: {'25':'010101'}
        for i in range(len(population)): #tính benefit của quần thể
            value = chromosome.calculate_value(my_data, population[i])
            d[value] = population[i]
        keys = sorted(d,reverse=True) #Mảng sắp xếp theo thứ tự giảm về KL
        new_d = {}
        for k in keys:
            #Lấy NST tương ứng với khối lượng
            new_d[k]=d[k]
        out = dict(itertools.islice(new_d.items(), 2*POPULATION)) # Cắt lấy 2*pop bộ NST đầu tiên
        return out # Trả về dict đã được sắp xếp theo thứ tự giảm dần của w

#Class thao thác với NST
class item_chromosome:
    def __init__(self):
        self.chromosome = []

    def combine(self, my_data, parent1, parent2, weight, chromosome, gene):
        """generation of new child chromosome""" # ghép nửa + đảo bit
        child = [0]*len(parent1)
        first_half = int(len(parent1) / 2)
        second_half = len(parent2) - first_half
        for i in range(first_half):
            child[i] = parent1[i]
        for i in range(first_half, first_half + second_half):
            child[i] = parent2[i]

        child = gene.mutate(child)
        while self.calculate_weight(my_data, child) > weight: # xoá những child > W
            child = chromosome.remove_item(child)
        return child

    def remove_item(self, chromosome):
        """removal of item if item exceeds weight"""
        # Đảo bit
        while True:
            bit = random.randint(0, len(chromosome) - 1)
            if chromosome[bit] == 1:
                chromosome[bit] = 0
                return chromosome

    def calculate_value(self, my_data, chromosome):
        """calculation of value of the chromosome"""
        '''
        Đầu vào là bộ (v,w) và bộ NST cần tính giá trị
        '''
        value = 0
        for i in range(len(chromosome)):
            if  chromosome[i] == 1:
                value += my_data[i, 0]
        return value

    def calculate_weight(self, my_data, chromosome):
        """calculation of weight of the chromosome"""
        weight = 0
        for i in range(len(chromosome)):
            weight += chromosome[i] * my_data[i, 1]
        return weight

#Class thao thác với gene
class item_gene:
    def __init__(self, my_data):
        self.gene = []

    def mutate(self, chromosome): # Đảo bit
        """mutation of single gene"""
        if random.uniform(0, 1) < MUTATION:
            bit = random.randint(0, len(chromosome)-1) # Chọn bit để đảo
            if chromosome[bit] == 0:
                chromosome[bit] = 1
            else:
                chromosome[bit] = 0
        return chromosome


def main():
    np.random.seed(0)
    max_weight = int(input("W = "))
    num_items = int(input("So do vat:"))
    input_data = np.random.uniform(size=(num_items,2))
    #input_data = np.round(input_data, decimals=1)
    print(input_data)
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    try:
        my_data = input_data
    except:
        print('Error in file read')
        logging.debug('Error in file open')
    # try:
    #     testknapsack = knapsack_population()
    #     testchromosome = item_chromosome()
    #     testgene = item_gene(my_data)

        #assert testknapsack.fitness(my_data,testknapsack,testchromosome)
        # #def fitness(self, my_data, population, chromosome)
        #assert testchromosome.combine(my_data,testchromosome,testchromosome,max_weight,testchromosome,testgene)
        # #def combine(self, my_data, parent1, parent2, weight, chromosome, gene):
        #assert testchromosome.calculate_value(my_data,testchromosome)
        # #def calculate_value(self, my_data, chromosome):
        #assert testchromosome.calculate_weight(my_data,testchromosome)
        #def calculate_weight(self, my_data, chromosome):
        #assert testgene.mutate(testchromosome)
        #def mutate(self, chromosome):

    # except:
    #     print('Error in asserts')
    #     logging.debug('Error in asserts')
    knapsack = knapsack_population() #init
    chromosome = item_chromosome() #init
    gene = item_gene(my_data) #init
    population = knapsack.create_population(my_data, max_weight, POPULATION) #random init 10 chromesome

    local_best = 0
    process = 0 # tính số lần ko tăng của best
    best = 0
    for i in range(LIMIT_ITERATION):
        # Khống chế kích thước của quần thể là n
        # In ra
        new_population = []

        population_scores = knapsack.fitness(my_data, population, chromosome) #dict có sx giảm dần KL
        best = max(population_scores.keys()) # lấy value max


        sorted_population = [] # Mảng các NST
        for k, v in population_scores.items(): #duyệt qua từng phần tử của dict
            sorted_population.append(population_scores[k]) # lấy các value ( chrmosome) ( có thứ tự giảm dần về value )
        for j in range(len(sorted_population) - 1):
            for m in range(len(sorted_population) - 1):
                if m != j:
                    #combine(self, my_data, parent1, parent2, weight, chromosome, gene):
                    child = chromosome.combine(my_data, sorted_population[j], sorted_population[m], max_weight,
                                               chromosome, gene)
                    new_population.append(child)

        population = new_population
        new_population_score = knapsack.fitness(my_data, population, chromosome) #dict có sx giảm dần KL
        local_best = max(new_population_score.keys())
        best = max(best,local_best) # Cập nhật giá trị best

        # if process > 100:
        #     print('Iteration: %d ' % i)
        #     print('Best Value found', np.round(local_best, decimals=1))
        #     print('Containing Chromosome Is', new_population_score[local_best])
        #     print('With Weight', chromosome.calculate_weight(my_data, new_population_score[local_best]))
        #     print('-----------------------------------------------------')
        #     break
        if (i % PRINT_PER_IT == 0): # Sau số iter nhất định
            print('Iteration: %d ' % i)
            print('Local Best Value found', local_best)
            print('Containing Chromosome Is', new_population_score[local_best])
            print('With Weight', chromosome.calculate_weight(my_data, new_population_score[local_best]))
            print('-----------------------------------------------------')
        if process <= CHANGE_PER_ITER:
            if (abs(best-local_best) < 0.01):
                process += 1
            else:
                process = 0
        else:
            global MUTATION
            MUTATION += 0.1
            process = 0
            print('Change mutation:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', MUTATION)

    #lambda x: len(new_population_score[x])

    print ('Best Value found', best)
    print ('Containing Chromosome Is', new_population_score[best])
    print ('With Weight',chromosome.calculate_weight(my_data, new_population_score[best]))

if __name__ == "__main__":
    main()
