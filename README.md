# READ.ME
##### 1.sequential_map 
    the function takes as arguments any number of functions as well as a container with some values, the function returns a list of the results of the sequential application of the passed functions to the values in the container.
##### 2.sequential_map 
    consensus_filter - the function  accepts as arguments any number of functions (
    positional arguments) that return True or False, as well as a container with some values. The function  returns a list of values which, when passed to all functions give True
##### 3.conditional_reduce
    The function must accepts 2 functions, as well as a container with values. The first function must take 1 argument and return True or False, the second also takes 2 arguments and returns a value return one value - the result of reduce, skipping the values with which the first function returned False.
##### 4. func_chain 
    the function must accept as arguments any number of functions  The function should return a function combining all passed by sequential execution.
##### 5. multiple_partial 
    multiple_partial is an analogue of the partial function, but which takes an unlimited number of functions as arguments and returns a list of the same number of "partial functions"
##### 6. print without print using sys module
