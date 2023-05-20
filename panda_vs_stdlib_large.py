import timeit
import pandas as pd
import random

# Let's prepare the dictionaries
# Each dictionary represents a row in a table
# The keys are the column names and the values are the data
dictionaries = [
    {
        f'column_{i}': random.random()
        for i in range(100)
    }
    for _ in range(1000)
]

# Define functions for each merging method

def merge_with_update():
    result = {}
    for d in dictionaries:
        result.update(d)
    return result

def merge_with_dict_comprehension():
    return {k: v for d in dictionaries for k, v in d.items()}

def merge_with_unpacking():
    result = {}
    for d in dictionaries:
        result = {**result, **d}
    return result

def merge_with_union():
    result = {}
    for d in dictionaries:
        result = result | d
    return result

def merge_with_pandas():
    df = pd.DataFrame(dictionaries)
    return df.to_dict()

# Now we'll time each method
update_time = timeit.timeit(merge_with_update, number=100)
dict_comprehension_time = timeit.timeit(merge_with_dict_comprehension, number=100)
unpacking_time = timeit.timeit(merge_with_unpacking, number=100)
union_time = timeit.timeit(merge_with_union, number=100)
pandas_time = timeit.timeit(merge_with_pandas, number=100)

# And print the results
print(f'update: {update_time} seconds')
print(f'dict comprehension: {dict_comprehension_time} seconds')
print(f'unpacking: {unpacking_time} seconds')
print(f'union: {union_time} seconds')
print(f'pandas: {pandas_time} seconds')
