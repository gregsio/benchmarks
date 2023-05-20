import matplotlib.pyplot as plt

methods = ['update', 'union', 'dict comprehension', 'unpacking', 'pandas']

# Averaged time values from your benchmarks
average_times_dataset_1 = [0.0032579898834228516, 0.004385709762573242, 0.006670713424682617, 0.010681867599487305, 0.06796979904174805]
average_times_dataset_2 = [0.0007576942443847656, 0.000736236572265625, 0.0013744831085205078, 0.0013728141784667969, 1.1770124435424805]

x = range(len(methods))

plt.figure(figsize=(12,6))

plt.bar(x, average_times_dataset_1, width=0.4, align='center', color='b', label='Dataset 1')
plt.bar(x, average_times_dataset_2, width=0.4, align='edge', color='r', label='Dataset 2')

plt.xlabel('Methods')
plt.ylabel('Time (seconds)')
plt.title('Benchmarking Results of Different Dictionary Merging Methods')
plt.xticks(x, methods, rotation=45)
plt.legend()
plt.tight_layout()

# Save the figure instead of trying to show it
plt.savefig('benchmark_results.png')
