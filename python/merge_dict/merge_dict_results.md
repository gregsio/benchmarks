# Python merge dictionaries benchmark

## Putting it all together 

![img](./benchmark_results.png)
![img](./benchmark_results_standard_lib.png)

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

## 1. Update Method
This method performed the best for both datasets. This can be attributed to the fact that `update()` is a built-in Python method implemented in C, which provides significant performance benefits. It modifies the dictionary in-place, reducing the need for additional memory allocation. It performs a direct system call to the `malloc()` and `free()` functions, bypassing the need for a Python interpreter and reducing overhead. The time complexity of this operation is generally O(1) for each key-value pair added.

## 2. Union (|) Method
This method, introduced in Python 3.9, provides a simple and readable syntax for merging dictionaries. However, it performs slightly worse than `update()`, as it creates a new dictionary instead of updating in place.

## 3. Dictionary Comprehension
This method was slightly slower than `update()` and `union()`. A dictionary comprehension involves more Python-level operations (like iteration and key/value assignments), making it slower than the other two methods. It generates a new dictionary, leading to extra memory allocation.

## 4. Unpacking (**)
This method was the slowest among the standard library methods. While it's a neat trick, it creates a new dictionary and involves Python-level iteration and assignments, which slows it down.

## 5. Using pandas
Pandas is significantly slower. It's not designed for this specific task, and its DataFrame structure is more complex and versatile than a simple dictionary. The conversion from dictionaries to a DataFrame and back to a dictionary adds significant overhead.

In conclusion, while each method has its own use cases, `update()` is the most efficient for merging dictionaries, especially when performance is a concern. The benefits are most noticeable when dealing with a large number of dictionaries with fewer keys, as in Dataset 1. If a new dictionary is needed and you are using Python 3.9+, the union operator (|) is a good alternative due to its simplicity and readability.

### Analysis and time complexity:

All of these methods have a linear time complexity, O(n), as they involve a full traversal of the input data. However, they differ in terms of their overheads and low-level operations, which contribute to the differences in their running times.

**`update()`**: This method is the fastest because it modifies the dictionary in place, avoiding the need for additional memory allocation. It is implemented in C, providing optimizations and reducing overhead.

**`union`**: This operator in Python 3.9+ also has a time complexity of O(n), as it needs to iterate over all keys and values in the input dictionaries. However, it is slightly slower than `update()` because it creates a new dictionary, involving memory allocation and initialization overheads.

**`Unpacking (**)`**: This method is slightly slower than the `union` operation, likely due to creating a new dictionary with every merge operation and possibly due to lower-level implementation details of the ** operator. However, it is still relatively fast due to being a built-in Python feature implemented in optimized C.

**`Dictionary Comprehension`**: This method creates a new dictionary and, for each item in the original dictionaries, adds a key-value pair to the new one. The overhead here is mainly due to creating new dictionaries and adding items to them. It involves more Python bytecode instructions and is less optimized compared to `update()`, `union`, and `**` methods.

**`Pandas`**: Although pandas is highly optimized for certain operations, it is slower than the built-in methods for this specific task due to its overheads. Constructing a DataFrame from dictionaries involves memory allocation and potential data conversions. Converting the DataFrame back to a dictionary also involves memory allocations and data conversions. These additional operations contribute to pandas being slower than the built-in methods.

In conclusion, while all these methods have a time complexity of O(n), the `update()` method is the fastest for merging dictionaries due to its in-place operation. It is followed by the `union` operator, the `Unpacking (**)` method, dictionary comprehension, and finally pandas. The slower methods involve additional memory allocation and initialization overheads, contributing to their longer running times. However, it's important to choose the right tool for the job: while `update()` is fastest for this specific task, other methods might be more suitable or efficient depending on the specific requirements of your application.

### Built-in Python feature and is implemented in optimized C

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

#### Time complexity for malloc and free()

In a simple and idealized model, the time complexity for `malloc()` and `free()` can be considered as constant time, O(1), meaning the time to perform these operations doesn't depend on the size of the memory being managed.

However, in practice, the actual time complexity of `malloc()` and `free()` depends on the implementation of the memory management system in the runtime environment and the operating system, as well as the state of the memory (for instance, how fragmented it is).

When a program calls malloc(), the memory management system needs to find a block of memory large enough to satisfy the request. The time it takes to find such a block can depend on several factors:

- The size of the request: For small sizes, memory managers often keep pools of fixed-size blocks ready to go, which can be allocated with constant time complexity. For larger sizes, the memory manager might need to search through a list of free blocks, which could take time proportional to the number of free blocks (linear time complexity).

- The state of the memory: If the memory is heavily fragmented, it might take longer to find a free block of the right size, even if there's enough total free memory.

The `free()` function can also have variable time complexity, depending on the memory management system's strategy for merging freed blocks with their neighbors to reduce fragmentation. This can involve searching through lists of blocks, which could potentially have linear time complexity.

Overall, while `malloc()` and `free()` can have constant time complexity in certain conditions, their actual performance can vary widely depending on various factors. The details of memory allocation and deallocation are complex and go beyond the usual scope of Big-O notation, which is a high-level abstraction used for analyzing algorithmic complexity.


## 1st benchmark results (archived code)

TODO: review and compare with results above

Results of 4 executions of the same benchmark.

| Method                | Execution 1 (s) | Execution 2 (s) | Execution 3 (s) | Execution 4 (s) |
|-----------------------|-----------------|-----------------|-----------------|-----------------|
| update()              | 0.2988          | 0.3234          | 0.3056          | 0.2874          |
| Dictionary Comprehension | 0.7252          | 0.7075          | 0.7318          | 0.7167          |
| Unpacking (**)        | 0.3314          | 0.3567          | 0.3296          | 0.3351          |
| union                 | 0.3339          | 0.3432          | 0.3282          | 0.3223          |
| Pandas                | 4.1233          | 3.8576          | 3.8797          | 3.9674          |

Now, averaging and sorting these results, we get:

| Method                   | Time (s) |
|--------------------------|----------|
| update()                 | 0.3038   |
| union                    | 0.3319   |
| Unpacking (**)           | 0.3382   |
| Dictionary Comprehension | 0.7203   |
| Pandas                   | 3.9570   |