import timeit
import pandas as pd

# Let's prepare the dictionaries
dictionaries = [{f'key_{i}': i for i in range(1000)} for _ in range(1000)]

def merge_with_pandas():
    dfs = [pd.DataFrame(list(d.items()), columns=['key', 'value']) for d in dictionaries]
    df_final = pd.concat(dfs).drop_duplicates('key', keep='last').set_index('key')
    return df_final.to_dict()['value']

# Time the function
pandas_time = timeit.timeit(merge_with_pandas, number=10)

# Print the results
print(f'pandas: {pandas_time} seconds')

