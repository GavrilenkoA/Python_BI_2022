import numpy as np

if __name__ == "__main__":
    var_1 = np.zeros((5, 5))
    var_2 = np.arange(10)
    var_3 = np.array([1, 2, 3])
    print(var_1, var_2, var_3)


def matrix_multiplication(a, b):
    '''
     необходимое условие перемножения матриц - это равенство строк А и столбцов B (или наоборот)
     при это умножается строка A на столбец B, то есть кол-во столбцов A == кол-ву строк B.
     если у них нет совпадения по размерности, то приводим к нему, если возможно.
    :param a: первая матрица
    :param b: вторая матрица
    :return: результат матричного произведения
    '''
    a_sh, b_sh = a.shape, b.shape  # получаем размерности входящих матриц
    check_dim = False
    if a_sh[1] == b_sh[0]:  # совпадения размерности столбцов A и строк B
        check_dim = True
    if a_sh == b_sh:  # если две матрицы имеют имеют одинаковую размерность: (4, 3) == (4, 3), то достаточно одну транспонировать (выберем первую)
        a = a.T
        check_dim = True
    if a_sh[0] == b_sh[
        0]:  # размерность строк A совпадает со cтроками B, а должны совпадать столбцы A -> транспонируем A
        a = a.T
        check_dim = True
    if a_sh[1] == b_sh[
        1]:  # размерность столбцов B совпадает со столбцами A, а должны совпадать строки B -> транспонируем B
        b = b.T
        check_dim = True
    if a_sh[0] == b_sh[
        1]:  # размерность строк A совпадает со столбцами B, а должно быть наоборот -> транспонируем и A, и B.
        a = a.T
        b = b.T
        check_dim = True
    if check_dim:  # если условие проверки размерностей выполняется, то возвращаем результат перемножения, если нет, функция будет возвращать None
        c = np.dot(a, b)
        return c



def multiplication_check(l):
    """
    Функция итерируется по списку с матрицами, если на каком-то этапе, matrix_multiplication вернет None, то все матрицы в списке нельзя перемножить
    :param l: список с матрицами
    :return: True/False
    """
    a = l[0]
    ans = True
    for i in range(1, len(l)):
        b = l[i]
        a = matrix_multiplication(a, b)
        if a is None:
            ans = False
            break
    return ans


# %%
def multiply_matrices(l):
    """
   Функция итерируется по списку с матрицами, если на каком-то этапе, matrix_multiplication вернет None, то дальнейшие вычисления прекращаются
   :param l: список с матрицами
   :return: dot product or None
   """
    a = l[0]
    for i in range(1, len(l)):
        b = l[i]
        a = matrix_multiplication(a, b)
        if a is None:
            break
    return a



def compute_2d_distance(a, b):
    """
    :param a: вектор 1
    :param b: вектор 2
    :return: счиатет растояние между n-мерными  векторами (в тч и двумерными)
    """
    dist = np.sum(np.square(a - b))
    return dist



def compute_multidimensional_distance(a, b):
    """
    аналогично функции compute_2d_distance
    """
    dist = np.sum(np.square(a - b))
    return dist



def get_all_pair(arr):
    """

    :param arr:  двумерная матрица
    :return: комбинации идексов всех строк (объектов)
    """
    all_pair = []   # список с кортежами со всевозможными парами объектов из массива
    all_obj = [i for i in range(1, len(arr) + 1)]  # получим индексы всех объектов из массива
    for i in range(len(all_obj)):
        for k in range(i, len(all_obj)):
            all_pair.append((all_obj[i], all_obj[k]))  # получим  индексы пары объектов и положим в список
    return all_pair



def compute_pair_distances(arr):
    dim_matrix_dist = len(arr)  # кол-во объектов в массиве
    dist = np.zeros((dim_matrix_dist, dim_matrix_dist)) # матрица размерности кол-ва объектов на кол-во объектов
    all_pair = get_all_pair(arr)
    for pair in all_pair:
        i, j = pair[0], pair[1]     # строки текущей пары
        r = compute_multidimensional_distance(arr[i - 1, :], arr[j - 1, :])     # слайс всех признаков текущих строк
        dist[i - 1, j - 1] = r  # кладем посчитанное расстояние на пересечение текущих объектов, пересечение симметрично относительно диагонали
        dist[j - 1, i - 1] = r
    return dist
