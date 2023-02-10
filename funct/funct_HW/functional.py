



import numpy as np


def sequential_map(*args):
    *funcs, collections = args
    for func in funcs:
        collections = map(func, collections)
    return list(collections)

sequential_map(np.square, np.sqrt, lambda x: x ** 3, [1, 2, 3, 4, 5])



def consensus_filter(*args):
    *funcs, collections = args
    for func in funcs:
        collections = filter(func, collections)
    return list(collections)



consensus_filter(lambda x: x > 0, lambda x: x > 5, lambda x: x < 10, [-2, 0, 4, 6, 11])





def conditional_reduce(*args):
    conditional_func, reduce_func, collection = args
    filtered_data = list(filter(conditional_func, collection))  #
    sum_val = filtered_data[0]  # выделим первое число из фильтрованной коллекции
    for i in range(1, len(filtered_data)):
        cur_el = filtered_data[i]  # получим текущее число из обновленной колекции
        sum_val = reduce_func(sum_val, cur_el)  # обновим сумму
    return sum_val



conditional_reduce(lambda x: x < 5, lambda x, y: x + y, [1, 3, 3, 5, 10])



def func_chain(*args):
    def merge(x):
        for funct in args:  # последовательно исполним функцию над аргументом друг за другом
            x = funct(x)
        return x

    return merge



my_chain = func_chain(lambda x: x + 2, lambda x: (x / 3, x // 3))
my_chain = func_chain(np.square, np.sqrt, lambda x: x ** 3)
my_chain(34)





def sequential_map(*args):
    '''
    Та же функция sequential_map, но уже с использованием func_chain
    '''
    *funcs, collections = args
    whole_func = func_chain(*funcs)
    collections = list(map(whole_func, collections))
    return collections


sequential_map(np.square, np.sqrt, lambda x: x ** 3, [1, 2, 3, 4, 5])


data = np.random.randint(5, size=(2, 2))    #сгенериуем матрицу для проверки

def partial(func, **kwargs):
    '''
    partial для одной функции
    :param func: изначальная функция
    :param kwargs: указываемые аргументы
    :return:
    '''

    def wrapper(x):
        return func(x, **kwargs)

    return wrapper



func = partial(np.max, axis=1)
func(data)



def multiple_partial(*args, **kwargs):
    list_part_func = []
    for func in args:  # используем partial для каждой функции из args
        part_func = partial(func, **kwargs)
        list_part_func.append(part_func)
    return list_part_func



a, b, c = multiple_partial(np.mean, np.max, np.sum, axis=1)

c(data) == np.sum(data, axis=1) #результаты равны



import sys




def priint(*args, sep=" ", end="\n", file=sys.stdout):
    ans = sep.join(map(str, args)) + end
    file.write(ans)







#%%
priint(5, "dsf", "fsdfsd", "rhfeg", sep='...', end="!")
