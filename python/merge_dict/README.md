# Python merge dictionaries benchmark

We are discussing various methods of merging Python dictionaries and testing their performance. The methods we've been comparing are:

- `update()`
- Dictionary Comprehension
- Unpacking (**)
- Union (|) (Python 3.9+)
- Using pandas

We created two different datasets for benchmarking these methods:

**Dataset 1:**
This dataset has a larger number of dictionaries, with each dictionary having smaller contents. Each dictionary in the dataset contains 100 keys, and their corresponding values are random, with the values either being an integer, a string, or an object.

**Dataset 2:**
This dataset has fewer dictionaries (1/10th of the first dataset), but each dictionary has a larger number of keys (1000 keys). All keys are strings, and the corresponding values are random floats.

| Method                | Dataset 1 (s) | Dataset 2 (s) |
|-----------------------|--------------|--------------|
| update()              | 0.00326      | 0.00076      |
| union                 | 0.00439      | 0.00074      |
| Dictionary Comprehension | 0.00667  | 0.00137      |
| Unpacking (**)        | 0.01068      | 0.00137      |
| Pandas                | 0.06797      | 1.17701      |

From these results, the `update()` method consistently performed the best. Let's go into a detailed analysis.

### 1. Update Method
This method performed the best for both datasets. This can be attributed to the fact that `update()` is a built-in Python method implemented in C, which provides significant performance benefits. It modifies the dictionary in-place, reducing the need for additional memory allocation. It performs a direct system call to the `malloc()` and `free()` functions, bypassing the need for a Python interpreter and reducing overhead. The time complexity of this operation is generally O(1) for each key-value pair added.

### 2. Union (|) Method
This method, introduced in Python 3.9, provides a simple and readable syntax for merging dictionaries. However, it performs slightly worse than `update()`, as it creates a new dictionary instead of updating in place.

### 3. Dictionary Comprehension
This method was slightly slower than `update()` and `union()`. A dictionary comprehension involves more Python-level operations (like iteration and key/value assignments), making it slower than the other two methods. It generates a new dictionary, leading to extra memory allocation.

### 4. Unpacking (**)
This method was the slowest among the standard library methods. While it's a neat trick, it creates a new dictionary and involves Python-level iteration and assignments, which slows it down.

### 5. Using pandas
Pandas is significantly slower. It's not designed for this specific task, and its DataFrame structure is more complex and versatile than a simple dictionary. The conversion from dictionaries to a DataFrame and back to a dictionary adds significant overhead.

In conclusion, while each method has its own use cases, `update()` is the most efficient for merging dictionaries, especially when performance is a concern. The benefits are most noticeable when dealing with a large number of dictionaries with fewer keys, as in Dataset 1. If a new dictionary is needed and you are using Python 3.9+, the union operator (|) is a good alternative due to its simplicity and readability.

## Analysis

All of these methods have a linear time complexity, O(n), as they involve a full traversal of the input data. However, they differ in terms of their overheads and low-level operations, which contribute to the differences in their running times.

**`update()`**: This method is the fastest because it modifies the dictionary in place, avoiding the need for additional memory allocation. It is implemented in C, providing optimizations and reducing overhead.

**`union`**: This operator in Python 3.9+ also has a time complexity of O(n), as it needs to iterate over all keys and values in the input dictionaries. However, it is slightly slower than `update()` because it creates a new dictionary, involving memory allocation and initialization overheads.

**`Unpacking (**)`**: This method is slightly slower than the `union` operation, likely due to creating a new dictionary with every merge operation and possibly due to lower-level implementation details of the ** operator. However, it is still relatively fast due to being a built-in Python feature implemented in optimized C.

**`Dictionary Comprehension`**: This method creates a new dictionary and, for each item in the original dictionaries, adds a key-value pair to the new one. The overhead here is mainly due to creating new dictionaries and adding items to them. It involves more Python bytecode instructions and is less optimized compared to `update()`, `union`, and `**` methods.

**`Pandas`**: Although pandas is highly optimized for certain operations, it is slower than the built-in methods for this specific task due to its overheads. Constructing a DataFrame from dictionaries involves memory allocation and potential data conversions. Converting the DataFrame back to a dictionary also involves memory allocations and data conversions. These additional operations contribute to pandas being slower than the built-in methods.

In conclusion, while all these methods have a time complexity of O(n), the `update()` method is the fastest for merging dictionaries due to its in-place operation. It is followed by the `union` operator, the `Unpacking (**)` method, dictionary comprehension, and finally pandas. The slower methods involve additional memory allocation and initialization overheads, contributing to their longer running times. However, it's important to choose the right tool for the job: while `update()` is fastest for this specific task, other methods might be more suitable or efficient depending on the specific requirements of your application.

## Time Complexity

When we talk about the time complexity of an operation, we usually describe it using Big O notation, which provides an upper bound on the time taken as a function of the input size.

For the task of merging dictionaries in Python, here are the rough Big O notations for each method:

- update(): O(n) - dict.update() method iterates over the keys and values of the dictionary to be merged, so its time complexity is proportional to the size of the input dictionaries.

- Dictionary comprehension: O(n) - This method also iterates over all keys and values in the input dictionaries, so its time complexity is also proportional to the size of the input. However, this method may be slower in practice than dict.update() because it involves creating a new dictionary.

- Union (| operator): O(n) - The union operator in Python 3.9+ also has a time complexity of O(n) for dictionaries because it needs to iterate over the keys and values in the input dictionaries. However, it creates a new dictionary in each operation, which can make it slower in practice than dict.update().

- Pandas: O(n) - Converting a list of dictionaries to a pandas DataFrame and then back to a dictionary also involves iterating over all the keys and values in the input dictionaries. However, pandas has additional overhead due to its more complex data structures and functionalities, which can make it slower in practice for this specific task.

In all these cases, the time complexity is O(n) because each method involves iterating over the keys and values in the input dictionaries. The differences in their actual running times largely come down to factors like memory allocation and object creation, the overhead of Python's high-level data structures and constructs, and the efficiencies of Python's underlying C implementation.

### Memory Allocation

Memory allocation can be a costly operation in terms of time complexity, and it depends on a variety of factors. Understanding the time complexity involves a little understanding of how memory is managed in systems.

When you request memory (for instance, when creating a new variable or object), the following steps typically occur:

   - The system checks if it has a sufficiently large block of contiguous free memory to satisfy the request.
   - If it finds such a block, it marks that block as used and returns a pointer to it.
   - If it doesn't find a free block that's large enough, it might need to perform a process called "garbage collection" to free up memory, or in some systems, it might even need to request more memory from the operating system.

Each of these steps takes time. The exact time depends on many factors, including the size of the memory request, the current state of the memory (for instance, how fragmented it is), the specifics of the system's memory management algorithms, and so on.

However, generally speaking, memory allocation can be considered an O(1) operation, meaning it takes a constant amount of time regardless of the size of the memory request. This is because the time it takes to allocate memory does not depend directly on the size of the memory block being allocated, but rather on factors like the state of the memory and the system's memory management algorithms. But in practice, memory allocation is often a relatively slow operation compared to other operations, especially in high-level languages like Python.

Now, when it comes to creating new objects like dictionaries in Python, there's additional overhead. This is because Python objects include additional information, like type information and reference counts, and creating these objects involves initializing this information and possibly calling object constructors. Furthermore, if the object being created is a collection like a dictionary or a list, additional memory needs to be allocated for the elements of the collection, which adds further time.

So, when you're creating a new dictionary for each merge operation, like in the dictionary comprehension method, you're performing this relatively costly memory allocation and object creation operation multiple times. In contrast, the update() method avoids this overhead by operating in-place on the existing dictionary. This is likely a significant factor in why update() is faster in these benchmarks.

### Built-in Python features are implemented in optimized C

`malloc()` and `free()` are functions in the C programming language used for dynamic memory management.

`malloc()`: The `malloc()` function stands for "memory allocation". It dynamically allocates a single large block of memory with the specified size. It initializes each block with a default garbage value. The function returns a pointer of type void, which can be cast into a pointer of any form. It takes the size (in bytes) of memory that needs to be allocated. If the space is insufficient, allocation fails and returns a NULL pointer.

Here's an example of `malloc()` usage:

```c
int *ptr;
ptr = (int*) malloc(100 * sizeof(int));
```

In this code, 100 * sizeof(int) bytes of memory is allocated in the heap, and the pointer to this memory is assigned to ptr. We can now use ptr as an array.

`free()`: The `free()` function in C provides a mechanism to release the block of memory that was previously allocated by `malloc()`, `calloc()`, or `realloc()` function. The `free()` function does not actually delete anything; it merely makes a note in the heap management system that the program is done with the block, and the block can be reused for later allocations.

Here's an example of `free()` usage:

```c
free(ptr);
```
This code releases the block of memory pointed to by ptr for future use.

These functions are essential in C and C++ programming, where the programmer has direct control over memory management. In higher-level languages like Python, memory management is handled automatically by the interpreter or runtime environment, but under the hood, similar mechanisms are at work when you create or delete objects. However, it's important to note that improper usage of `malloc()` and `free()` can lead to issues like memory leaks and dangling pointers, which are common sources of bugs in C and C++ programs.

### Time complexity for malloc and free()

In a simple and idealized model, the time complexity for `malloc()` and `free()` can be considered as constant time, O(1), meaning the time to perform these operations doesn't depend on the size of the memory being managed.

However, in practice, the actual time complexity of `malloc()` and `free()` depends on the implementation of the memory management system in the runtime environment and the operating system, as well as the state of the memory (for instance, how fragmented it is).

When a program calls malloc(), the memory management system needs to find a block of memory large enough to satisfy the request. The time it takes to find such a block can depend on several factors:

- The size of the request: For small sizes, memory managers often keep pools of fixed-size blocks ready to go, which can be allocated with constant time complexity. For larger sizes, the memory manager might need to search through a list of free blocks, which could take time proportional to the number of free blocks (linear time complexity).

- The state of the memory: If the memory is heavily fragmented, it might take longer to find a free block of the right size, even if there's enough total free memory.

The `free()` function can also have variable time complexity, depending on the memory management system's strategy for merging freed blocks with their neighbors to reduce fragmentation. This can involve searching through lists of blocks, which could potentially have linear time complexity.

Overall, while `malloc()` and `free()` can have constant time complexity in certain conditions, their actual performance can vary widely depending on various factors. The details of memory allocation and deallocation are complex and go beyond the usual scope of Big-O notation, which is a high-level abstraction used for analyzing algorithmic complexity.

## Benchmark Method and Raw Results

![img](./benchmark_results.png)
![img](./benchmark_results_standard_lib.png)

### Datatasets


Certainly, here's a summary of all the datasets used, alongside how each one was generated in Python.

1. **Initial Dataset:**

    This dataset consisted of 100 simple dictionaries, each containing 10 integer keys with integer values. These were generated using the following Python code:

    ```python
    dictionaries = [
        {i: i for i in range(10)}
        for _ in range(100)
    ]
    ```

| Method | Average Time (seconds) |
| --- | --- |
| `update` | 0.30863 |
| `dictionary comprehension` | 0.72028 |
| `unpacking` | 0.33820 |
| `union` | 0.34658 |
| `pandas` | 3.95675 |

2. **Complex Dictionaries Dataset 1:**

    This dataset consisted of 100 dictionaries, each containing 100 keys. The keys were random strings of lengths between 1 and 20, and the values were a mix of integers, strings, and custom `Object` instances. This dataset was generated using:

    ```python
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
    ```

| Method | Time (seconds) |
| --- | --- |
| `update` | 0.00326 |
| `dictionary comprehension` | 0.00667 |
| `unpacking` | 0.01068 |
| `union` | 0.00439 |
| `pandas` | 0.06797 |

3. **Complex Dictionaries Dataset 2:**

    This dataset consisted of 1,000 dictionaries, each containing 100 keys. Each key was prefixed with the string 'column_' followed by an integer, and the values were random floating-point numbers. This dataset was generated using:

    ```python
    dictionaries = [
        {
            f'column_{i}': random.random()
            for i in range(100)
        }
        for _ in range(1000)
    ]
    ```

| Method | Time (seconds) |
| --- | --- |
| `update` | 0.00076 |
| `dictionary comprehension` | 0.00137 |
| `unpacking` | 0.00137 |
| `union` | 0.00074 |
| `pandas` | 1.17701 |

### Final Benchmark

#### Dataset 1

| Method | Time (seconds) |
| --- | --- |
| `update` | 0.00326 |
| `dictionary comprehension` | 0.00667 |
| `unpacking` | 0.01068 |
| `union` | 0.00439 |
| `pandas` | 0.06797 |

#### Dataset 2

| Method | Time (seconds) |
| --- | --- |
| `update` | 0.00076 |
| `dictionary comprehension` | 0.00137 |
| `unpacking` | 0.00137 |
| `union` | 0.00074 |
| `pandas` | 1.17701 |


Each of these datasets represents different potential use cases, allowing us to test the performance of the different merging methods under a variety of conditions. Note that the specific performance may vary depending on the characteristics of the data and the computational environment.

### Unpacking Using ** VS Dict Comprehension

Let's consider two dictionaries that we want to merge:

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
```

To merge these two dictionaries using unpacking (`**`), you'd use the following syntax:

```python
merged_dict = {**dict1, **dict2}
```

`merged_dict` will now be `{'a': 1, 'b': 2, 'c': 3, 'd': 4}`.

The `**` operator is used to unpack the keys and values from each dictionary into a new dictionary.

On the other hand, to merge these dictionaries using dictionary comprehension, you would use this syntax:

```python
merged_dict = {k: v for d in [dict1, dict2] for k, v in d.items()}
```

`merged_dict` will again be `{'a': 1, 'b': 2, 'c': 3, 'd': 4}`.

In this case, the dictionary comprehension iterates over a list of the dictionaries to be merged (`[dict1, dict2]`), and for each dictionary, it iterates over its keys and values (`k, v in d.items()`) to create the new dictionary.

So the primary syntactical difference is that the unpacking method uses the `**` operator to unpack the dictionaries into a new one, while the dictionary comprehension method uses a loop to iterate over the keys and values of the dictionaries. Both methods result in a new dictionary that is a merged version of the input dictionaries.


### Dictionary Comprehension VS Unpacking (`**`) method

Absolutely, here are the averaged results rounded to 5 decimal places for dictionary comprehension and unpacking methods from all the benchmarks:

1. **Dictionary Comprehension:**

First Set of Benchmarks:
- Run 1: 0.72516 seconds
- Run 2: 0.70749 seconds
- Run 3: 0.73180 seconds
- Run 4: 0.71666 seconds
- Average: 0.72028 seconds

Final Set of Benchmarks:
- Dataset 1: 0.00667 seconds
- Dataset 2: 0.00137 seconds
- Average: 0.00402 seconds

2. **Unpacking (`**`) method:**

First Set of Benchmarks:
- Run 1: 0.33141 seconds
- Run 2: 0.35671 seconds
- Run 3: 0.32961 seconds
- Run 4: 0.33509 seconds
- Average: 0.33820 seconds

Final Set of Benchmarks:
- Dataset 1: 0.01068 seconds
- Dataset 2: 0.00137 seconds
- Average: 0.00603 seconds

These results reflect the performance of each method under different circumstances. Both methods significantly speed up with smaller, less complex datasets. However, the dictionary comprehension method is generally slower than the unpacking method, likely due to the overhead of Python-level iteration and key-value assignments involved in dictionary comprehension.

The difference in performance between unpacking and the union operator in different benchmarks can be attributed to the nature of the datasets we used for these benchmarks, as well as some specific characteristics of these two methods.

The union (|) operator and the unpacking (**) method have the same time complexity - O(N), where N is the total size of the dictionaries. However, their performance can vary depending on the specific characteristics of the data and Python's memory management and optimization mechanisms.

Here's a more in-depth explanation:

- Size and Structure of Dictionaries:
In our first benchmarks, we used larger dictionaries. The union operator can be slower with larger dictionaries as it constructs a new dictionary and checks for key collisions. The unpacking method, on the other hand, could be faster because it relies on the built-in update mechanism when encountering a key collision.
The structure of the dictionaries can also affect the results. If there are more common keys in the dictionaries, the union operation could be slower due to the increased number of key collisions, while the unpacking method would benefit from the internal optimization of the update() method.

- Python's Memory Management:
Python's memory allocation strategy could also play a role. When a new dictionary is created, Python may allocate more memory than necessary to accommodate additional elements. This over-allocation can lead to more efficient code execution when the size of the dictionary grows, but may also result in a slower operation if the final size of the dictionary is significantly smaller than the allocated size.

In our later benchmarks, where the dictionaries were smaller, the performance difference between the unpacking and the union operator became smaller. This can be attributed to the reduced impact of memory allocation and key collision checking with smaller dictionary sizes.

It's important to note that while these micro-benchmarks provide valuable insights into the performance of different methods, they may not always translate directly to real-world applications, where the complexity and structure of the data, as well as the overall program logic, can greatly influence performance.

