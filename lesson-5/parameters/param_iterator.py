from functools import reduce
from itertools import product


def param_iterator(param_grid, verbose=False):
    param_names = param_grid.keys()
    param_values = param_grid.values()
    if (verbose):
        number_of_combinations = reduce(
            lambda a, b: a*b, [len(params) for name, params in param_grid.items()])
        step = 0
    for prod in product(*param_values):
        current_params = dict(zip(param_names, prod))
        if (verbose):
            print(f"Step {step} of {number_of_combinations}")
            print(f"Parameters: {current_params}")
            step += 1
        yield current_params
