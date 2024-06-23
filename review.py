# Review 1

def add_to_list(value, my_list=[]):
    # my_list is a reference to the same list which will be updated every time this function is called
    # it's misleading to use an empty list as the default value, even though this function does work
    my_list.append(value)

    return my_list


add_to_list(1)
add_to_list(2)
res = add_to_list(3)


# Review 1's Fix
# Use closure to do the trick, avoid to use an empty array
def create_a_new_list_adder():
    my_list = []

    def add_to_list(value):
        my_list.append(value)
        return my_list

    return add_to_list


# Whenever need to add some elements to a new list, call this function
add_to_list = create_a_new_list_adder()
add_to_list(1)
add_to_list(2)
my_list = add_to_list(3)
print(f"Review 1 my_list should be [1, 2, 3]: {my_list}")


# Review 2

def format_greeting(name, age):
    # missing the format string method or use the f-string
    return "Hello, my name is {name} and I am {age} years old."


print("\nReview 2's result before being fixed: ", format_greeting("Jane", 12))


# Review 2's Fix
def format_greeting(name, age):
    # missing the format string method or use the f-string
    return f"Hello, my name is {name} and I am {age} years old."


print("Review 2's result after being fixed: ", format_greeting("Jane", 12))


# Review 3

class Counter:
    # This is the attr of class, has nothing to do with self.count
    # And this class cannot functional as a Counter
    count = 0

    def __init__(self):
        # self.count and Counter.count are saved in two different piece memory
        # self.count would always be 1 because each instance would be initialized once
        self.count += 1

    def get_count(self):
        return self.count


# Counter.count is not self.count
counter = Counter()
print("\nReview 3, Counter.count is counter.count?: ", Counter.count is counter.count)
print("Review 3 memory address of Counter.count: ", id(Counter.count))
print("Review 3 memory address of counter.count: ", id(counter.count))


# Review 3's Fix
class Counter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count


counter = Counter()
for _ in range(4):
    counter.increment()
print("Review 3's result after being fixed (after being incremented for 4 times): ", counter.get_count())

# Review 4
# Before Python 3.10, Python's threading is not inherently thread-safe.
# A lock is required if you want to run following tasks with multiple threads.

# ATTENTION!!!
# After Python 3.10, this class actually works, but it's an unexpected behavior.
# Check more details in the commit: https://github.com/python/cpython/commit/4958f5d69dd2bf86866c43491caf72f774ddec97
# Discussion on twitter: https://x.com/Yhg1s/status/1460935209059328000

import threading


class SafeCounter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def worker(counter):
    for _ in range(1000):
        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)

for t in threads:
    t.join()


print("\nReview 4's result before being fixed(could be correct sometimes): ", counter.count)
print("Recommend to increase the increment times to 100000 to see the incorrect result")


# Review 4's Fix (For Python < 3.10)

class SafeCounter:

    def __init__(self):
        self.count = 0
        self.mutex = threading.Lock()

    def increment(self):
        with self.mutex:
            self.count += 1


counter = SafeCounter()

threads = []

for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)

for t in threads:
    t.join()


print("Review 4's result after being fixed (always correct): ", counter.count)


# Review 5

def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            # This is a bug, all the counts would be 1
            # This row should be counts[item] += 1
            counts[item] = + 1
        else:
            counts[item] = 1
    return counts


lst = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
result = count_occurrences(lst)
print("\nReview 5's result before being fixed: ", result)


# Review 5's Fix

def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts


result = count_occurrences(lst)
print("Review 5's result after being fixed: ", result)
