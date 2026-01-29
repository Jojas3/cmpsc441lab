"""
Python Generator Functions Exercise
====================================

This exercise helps you understand generator functions in Python - a powerful
feature for creating iterators that produce values lazily (on-demand).

Learning Objectives:
- Understand the difference between return and yield
- Create generator functions using yield
- Use next() to retrieve values one at a time from a generator
- Understand how generators maintain state between calls
"""


# ============================================================================
# PART 1: Understanding Generators (Examples)
# ============================================================================

# A regular function returns ALL values at once (eager evaluation)
def get_squares_list(n):
    """Return a list of squares from 0 to n-1."""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


# A generator function YIELDS values one at a time (lazy evaluation)
def get_squares_generator(n):
    """Yield squares from 0 to n-1, one at a time."""
    for i in range(n):
        yield i ** 2


# Example usage - both produce the same values, but differently!
print("List version (all at once):", get_squares_list(5))
print("Generator version (lazy):", list(get_squares_generator(5)))

# Key difference: generators don't store all values in memory
# This matters when dealing with large datasets!


# ============================================================================
# PART 2: Using next() with Generators
# ============================================================================

# IMPORTANT: In upcoming labs, you'll use generators with next() to get
# values one at a time. This is how AI/LLM streaming responses work!

def countdown(n):
    """A simple generator that counts down from n to 1."""
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n  # Pause here and return n
        n -= 1   # Resume here on next() call
    print("Blastoff!")


# Demonstrate step-by-step execution with next()
print("\n--- Step-by-step generator execution with next() ---")
counter = countdown(3)
print(f"Created generator: {counter}")
print(f"First next(): {next(counter)}")   # Prints "Starting countdown", yields 3
print(f"Second next(): {next(counter)}")  # Resumes, yields 2
print(f"Third next(): {next(counter)}")   # Resumes, yields 1
# Next call would print "Blastoff!" and raise StopIteration
# Uncomment to see: print(f"Fourth next(): {next(counter)}")


# Another example: a generator that remembers state
def alternator():
    """Yields 'A' then 'B' then 'A' then 'B'... forever."""
    while True:
        yield "A"
        yield "B"


print("\n--- Alternator with next() ---")
alt = alternator()
print(f"next(alt) = {next(alt)}")  # A
print(f"next(alt) = {next(alt)}")  # B
print(f"next(alt) = {next(alt)}")  # A
print(f"next(alt) = {next(alt)}")  # B


# ============================================================================
# PART 3: YOUR EXERCISES
# ============================================================================

# TODO Exercise 1: Create an infinite counter generator
#
# Create a generator that yields numbers starting from `start`, incrementing
# by 1 each time next() is called. This generator never stops!
#
# Usage pattern (how it will be tested):
#     counter = infinite_counter(10)
#     next(counter)  # returns 10
#     next(counter)  # returns 11
#     next(counter)  # returns 12
#     ...continues forever...
#
def infinite_counter(start=0):
    """
    Yield numbers starting from start, incrementing by 1 forever.
    
    Args:
        start: The starting number (default 0)
    
    Yields:
        int: The next number in the sequence
    """
    # YOUR CODE HERE
    pass


# TODO Exercise 2: Create a cycling generator
#
# Create a generator that cycles through a list of items forever.
# Each call to next() returns the next item, wrapping around to the
# beginning when it reaches the end.
#
# Usage pattern (how it will be tested):
#     colors = color_cycle(["red", "green", "blue"])
#     next(colors)  # returns "red"
#     next(colors)  # returns "green"
#     next(colors)  # returns "blue"
#     next(colors)  # returns "red" (wraps around!)
#     next(colors)  # returns "green"
#     ...continues forever...
#
def color_cycle(items):
    """
    Yield items from the list in order, cycling back to start when exhausted.
    
    Args:
        items: A list of items to cycle through
    
    Yields:
        The next item in the cycle
    """
    # YOUR CODE HERE
    pass


# TODO Exercise 3: Create a take_n function that extracts n values from a generator
#
# This function takes a generator and a number n, and returns a LIST of
# the next n values from that generator. This is useful for getting a
# specific number of values from an infinite generator.
#
# Usage pattern (how it will be tested):
#     counter = infinite_counter(0)
#     take_n(counter, 5)  # returns [0, 1, 2, 3, 4]
#     take_n(counter, 3)  # returns [5, 6, 7] (continues from where it left off!)
#
#     colors = color_cycle(["A", "B"])
#     take_n(colors, 5)  # returns ["A", "B", "A", "B", "A"]
#
def take_n(generator, n):
    """
    Extract the next n values from a generator and return them as a list.
    
    Args:
        generator: A generator to pull values from
        n: Number of values to extract
    
    Returns:
        list: A list containing the next n values from the generator
    """
    # YOUR CODE HERE
    pass


# ============================================================================
# Why This Matters for Upcoming Labs
# ============================================================================

# In AI/LLM applications, responses are often streamed token by token.
# The pattern looks like this:
#
#     response_generator = llm.generate("Tell me a story")
#     
#     # Option 1: Process tokens one at a time
#     for token in response_generator:
#         print(token, end="", flush=True)
#     
#     # Option 2: Get tokens manually with next()
#     first_token = next(response_generator)
#     second_token = next(response_generator)
#
# Understanding generators and next() is essential for working with
# streaming AI responses!


# ============================================================================
# Run with: pytest tests/test_generator_exercise.py -v
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Run tests with: pytest tests/test_generator_exercise.py -v")
    print("=" * 50)
