import utils
import random
import argparse
import tsp_ga as ga
import numpy as np


def run(args):
    genes = utils.get_genes_from(args.cities_fn) 

    if args.verbose: # Chế độ in chi tiết
        print("-- Running TSP-GA with {} cities --".format(len(genes)))

    history = ga.run_ga(genes, args.pop_size, args.n_gen,
                        args.tourn_size, args.mut_rate, args.verbose)

    if args.verbose:
        print("-- Drawing Route --")

    utils.plot(history['cost'], history['route'])

    if args.verbose:
        print("-- Done --")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--pop_size', type=int, default=500, help='Population size')
    parser.add_argument('--tourn_size', type=int, default=50, help='Tournament size')
    parser.add_argument('--mut_rate', type=float, default=0.02, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Number of equal generations before stopping')
    parser.add_argument('--cities_fn', type=str, default="D:/Năm 5/Kì 2/A.I/Fund_AI_Course-master/chapter3/Development/TSP-GA-master/data/cities.csv", help='Data containing the geographical coordinates of cities')

    random.seed(2023)
    args = parser.parse_args()

    if args.tourn_size > args.pop_size:
        raise argparse.ArgumentTypeError('Tournament size cannot be bigger than population size.')

    run(args)