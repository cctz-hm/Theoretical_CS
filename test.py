list = [1, 2, 3]
# print(list)

def subsets(list, start=0): 
    if start == len(list): 
        return [[]]
    
    n_subset = subsets(list, start+1)
    return [[list[start]] + element for element in n_subset] + n_subset


output = subsets(list)
print("Recursion:", output)
print(len(output))

# task: using only letters from A-H, make 5 letter words that exist 
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]

'''
Planning 
- create a list of all possible 5 letter words and then eliminate and find words that work 

Class Notes 
- tempting to loop through lens (n number of loops) --> recursion 
- enumerate based on particular ordering of list 
    - empty list 
    []
    [] union [1]
    [],[1] union [2][1,2]
    ... 
- bit listing 
    - count numbers in binary and for each there is some number of 1s 
    - each of those ones are memorship indicator of specific element in subset 
    - each number up to n, the binary number of 2^n 
    - bitwise and of number with only one 1 and other zeros 
    - count 0 up to 2^n 
    - one that have match will be the one that includes the element 

'''




    
