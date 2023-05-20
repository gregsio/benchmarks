import time
import pandas as pd
import random
import string

class Object:
    """A simple class with two attributes."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

def random_string(length):
    """
    Generates a random string of the given length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Merging dictionaries using dict.update
def dict_method_update(dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result

# Merging dictionaries using dictionary comprehension
def dict_method_comprehension(dicts):
    return {k: v for d in dicts for k, v in d.items()}

# Merging dictionaries using the unpacking operator **
def dict_method_unpacking(dicts):
    return {k: v for d in dicts for k, v in d.items()}

# Merging dictionaries using the | operator (Python 3.9+)
def dict_method_union(dicts):
    result = {}
    for d in dicts:
        result |= d
    return result

# Merging dictionaries using pandas
def pandas_method(dicts):
    df = pd.DataFrame(dicts)
    return df.to_dict()

# Dataset 1: This dataset contains 1000 dictionaries, 
# each containing 100 key-value pairs. The keys are strings, 
# and the values are random floats. This dataset is designed 
# to test the performance of the methods when dealing with 
# a large number of simple, consistent dictionaries.
dictionaries1 = [
    {
        f'column_{i}': random.random()
        for i in range(100)
    }
    for _ in range(1000)
]

# Dataset 2: This dataset contains 100 dictionaries, 
# each containing 100 key-value pairs. The keys are random 
# strings of varying lengths, and the values are a mix of 
# integers, random strings, and instances of a simple custom 
# class. This dataset is designed to test the performance 
# of the methods when dealing with smaller, more complex 
# and diverse dictionaries.
dictionaries2 = [
    {
        random_string(random.randint(1, 20)): random.choice([
            random.randint(1, 100),
            random_string(random.randint(1, 20)),
            Object(random.randint(1, 100), random.randint(1, 100))
        ])
        for _ in range(100)
    }
    for _ in range(100)
]

datasets = {'Dataset 1': dictionaries1, 'Dataset 2': dictionaries2}

# Define the methods to be benchmarked.
methods = {
    'update': dict_method_update,
    'dict comprehension': dict_method_comprehension,
    'unpacking': dict_method_unpacking,
    'union': dict_method_union,
    'pandas': pandas_method,
}

# Benchmark each method with each dataset.
for dataset_name, dataset in datasets.items():
    print(f'\nBenchmarking with {dataset_name}:')
    for method_name, method in methods.items():
        start_time = time.time()
        method(dataset)
        elapsed_time = time.time() - start_time
        print(f'{method_name}: {elapsed_time} seconds')
