"""
Ciana Tzuo 

Book: Sherlock Holmes
File: sherlock.txt

Sources: 
https://www.geeksforgeeks.org/dsa/huffman-coding-greedy-algo-3/ 
https://www.w3schools.com/dsa/dsa_ref_huffman_coding.php 
https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Huffman.html 
https://realpython.com/ref/glossary/ascii/ 
https://docs.python.org/3/tutorial/inputoutput.html 
https://docs.python.org/3/library/heapq.html 
https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/ 
https://www.geeksforgeeks.org/python/ways-sort-list-dictionaries-values-python-using-lambda-function/

"""

import heapq    # priority queue module 
import math

# Task 3: TreeVertex class
class TreeVertex:
    def __init__(self, c=None, weight=0):
        self.c = c
        self.weight = weight
        self.leftChild = None
        self.rightChild = None
        self.height = 0 

    def is_leaf(self):
        return self.leftChild is None and self.rightChild is None


# Task 2: countFrequencies()
def countFrequencies(filename):
    """
    Counts ASCII characters
    Returns dictionary: char -> count
    """
    freqs = {}

    f = open(filename, "r", encoding="utf-8", errors="replace")

    for line in f:
        for ch in line:
            # Keep only ASCII characters
            if ord(ch) < 128:
                if ch in freqs:
                    freqs[ch] += 1
                else:
                    freqs[ch] = 1

    f.close()
    return freqs


def printFrequencyMap(freqs):
    """
    Prints the frequency map from highest frequency to lowest
    """
    print("\n--- Task 2: Frequency Map ---")

    # Sort by frequency descending
    sorted_items = sorted(freqs.items(), key=lambda item: item[1], reverse=True)

    for ch, count in sorted_items:
        print(f"{repr(ch):>6} (ASCII {ord(ch):3}) -> {count}")


# Task 4: buildTree(freqs)
def buildTree(freqs):
    """
    Builds a Huffman tree using a PriorityQueue (min-heap).

    freqs: dictionary mapping character -> frequency

    Returns:
        A TreeVertex object that is the root of the Huffman tree.
    """
    pq = []     # min-heap priority queue
    counter = 0  # ensures that we do not compare TreeVertex objects directly

    # Put each character into the PriorityQueue as a leaf node
    for ch in freqs:
        node = TreeVertex(ch, freqs[ch])
        heapq.heappush(pq, (node.weight, counter, node))
        counter += 1

    # Edge case: no ASCII characters
    if len(pq) == 0:
        return None

    # Edge case: only one distinct character
    if len(pq) == 1:
        return pq[0][2]

    # Remove two lowest-weight nodes and merge 
    while len(pq) > 1:
        w1, _, left = heapq.heappop(pq)
        w2, _, right = heapq.heappop(pq)

        parent = TreeVertex(None, w1 + w2)
        parent.leftChild = left
        parent.rightChild = right

        heapq.heappush(pq, (parent.weight, counter, parent))
        counter += 1

    # The last node is the root
    root = heapq.heappop(pq)[2]
    return root


# Task 5: createCodeMap(root)

def createCodeMap(root):
    """
    Uses the Huffman tree to build a dictionary:
        char -> bitstring
    Left = "0", Right = "1"
    """
    code_map = {}

    if root is None:
        return code_map

    # Edge case: only one leaf in the whole tree
    if root.is_leaf():
        code_map[root.c] = "0"
        return code_map

    def walk(node, current_bits):
        # If leaf, store
        if node.is_leaf():
            code_map[node.c] = current_bits
            return

        # Otherwise keep walking
        if node.leftChild is not None:
            walk(node.leftChild, current_bits + "0")
        if node.rightChild is not None:
            walk(node.rightChild, current_bits + "1")

    walk(root, "")
    return code_map


def printCodeMap(code_map):
    """
    Prints the code map 
    """
    print("\n--- Task 5: Code Map ---")
    for ch in sorted(code_map.keys(), key=lambda x: ord(x)):
        print(f"{repr(ch):>6} (ASCII {ord(ch):3}) -> {code_map[ch]}")


# Question 1 & 2 
def huffman_total_bits(freqs, code_map):
    """
    Question 1:
    Total Huffman bits = sum(freq[ch] * len(code_map[ch])) for all characters
    """
    total = 0
    for ch in freqs:
        total += freqs[ch] * len(code_map[ch])
    return total


def fixed_length_bits_per_char(num_distinct_chars):
    """
    Question 2:
    Minimum fixed bits per char = ceil(log2(k))
    where k = number of distinct characters
    """
    if num_distinct_chars <= 1:
        return 1
    return math.ceil(math.log2(num_distinct_chars))


def fixed_length_total_bits(total_chars, bits_per_char):
    """
    Question 2:
    Total fixed bits = total_chars * bits_per_char
    """
    return total_chars * bits_per_char


# Run everything
def main():
    filename = "sherlock.txt"

    # Task 2
    freqs = countFrequencies(filename)
    printFrequencyMap(freqs)

    # Task 4
    root = buildTree(freqs)
    if root is None:
        print("No ASCII characters were counted. Check your file.")
        return
    print("\nTask 4: Huffman tree built")

    # Task 5
    code_map = createCodeMap(root)
    printCodeMap(code_map)
    print("\nTask 5: Code map created.")

    # Question 1 and 2
    total_chars = sum(freqs.values())
    num_distinct = len(freqs)

    # Question 1: Huffman bits
    huff_bits = huffman_total_bits(freqs, code_map)

    # Question 2: fixed-length encoding bits
    fixed_bits_per = fixed_length_bits_per_char(num_distinct)
    fixed_bits_total = fixed_length_total_bits(total_chars, fixed_bits_per)

    savings = fixed_bits_total - huff_bits

    print("\n================= QUESTIONS =================")
    print("Question 1:")
    print(f"Total Huffman bits needed = {huff_bits}")

    print("\nQuestion 2:")
    print(f"Distinct ASCII characters (k) = {num_distinct}")
    print(f"Minimum fixed bits per character = {fixed_bits_per}")
    print(f"Total ASCII characters counted = {total_chars}")
    print(f"Fixed-length total bits needed = {fixed_bits_total}")
    print(f"Space saved = {savings} bits")

if __name__ == "__main__":
    main()