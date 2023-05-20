import timeit
import random
import string
from collections import namedtuple

# Let's use a namedtuple for our objects
Object = namedtuple('Object', 'x y')

# Function to generate a random string
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Let's prepare the dictionaries
dictionaries = [
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

# Define functions for each merging method

def merge_with_update():
    result = {}
    for d in dictionaries:
        result.update(d)
    return result

def merge_with_unpack():
    result = {k: v for d in dictionaries for k, v in d.items()}
    return result

def merge_with_union():
    result = {}
    for d in dictionaries:
        result = result | d
    return result

# Now we'll time each method
update_time = timeit.timeit(merge_with_update, number=100)
unpack_time = timeit.timeit(merge_with_unpack, number=100)
union_time = timeit.timeit(merge_with_union, number=100)

# And print the results
print(f'update: {update_time} seconds')
print(f'unpack: {unpack_time} seconds')
print(f'union: {union_time} seconds')
