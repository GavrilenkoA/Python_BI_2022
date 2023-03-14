#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/GavrilenkoA/Python_BI_2022/blob/iterators/%D0%9A%D0%BE%D0%BF%D0%B8%D1%8F_%D0%B1%D0%BB%D0%BE%D0%BA%D0%BD%D0%BE%D1%82%D0%B0_%22HW_2_ipynb%22.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Задание 1 (2 балла)

# Напишите класс `MyDict`, который будет полностью повторять поведение обычного словаря, за исключением того, что при итерации мы должны получать и ключи, и значения.
# 
# **Модули использовать нельзя**

# In[ ]:





# In[17]:


class MyDict(dict):
    def __iter__(self):
        for key, value in self.items():
            yield (key, value)


# In[18]:


dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})
for key, value in dct:
    print(key, value)  


# In[19]:


for key, value in dct.items():
    print(key, value)


# In[20]:


for key in dct.keys():
    print(key)


# In[21]:


dct["c"] + dct["d"]


# # Задание 2 (2 балла)

# Напишите функцию `iter_append`, которая "добавляет" новый элемент в конец итератора, возвращая итератор, который включает изначальные элементы и новый элемент. Итерироваться по итератору внутри функции нельзя, то есть вот такая штука не принимается
# ```python
# def iter_append(iterator, item):
#     lst = list(iterator) + [item]
#     return iter(lst)
# ```
# 
# **Модули использовать нельзя**

# In[22]:


def iter_append(iterator, item):
    yield from iterator
    yield item



# In[23]:


my_iterator = iter([1, 2, 3])
new_iterator = iter_append(my_iterator, 4)

for element in new_iterator:
    print(element)


# # Задание 3 (5 баллов)

# Представим, что мы установили себе некоторую библиотеку, которая содержит в себе два класса `MyString` и `MySet`, которые являются наследниками `str` и `set`, но также несут и дополнительные методы.
# 
# Проблема заключается в том, что библиотеку писали не очень аккуратные люди, поэтому получилось так, что некоторые методы возвращают не тот тип данных, который мы ожидаем. Например, `MyString().reverse()` возвращает объект класса `str`, хотя логичнее было бы ожидать объект класса `MyString`.
# 
# Найдите и реализуйте удобный способ сделать так, чтобы подобные методы возвращали экземпляр текущего класса, а не родительского. При этом **код методов изменять нельзя**
# 
# **+3 дополнительных балла** за реализацию того, чтобы **унаследованные от `str` и `set` методы** также возвращали объект интересующего нас класса (то есть `MyString.replace(..., ...)` должен возвращать `MyString`). **Переопределять методы нельзя**
# 
# **Модули использовать нельзя**

# In[ ]:


class MyString(str):

  def wrapper(func):
    def inner_func(self):
      return MyString(func(self))
    return inner_func

  @wrapper
  def reverse(self):
      return self[::-1]
  
  @wrapper
  def make_uppercase(self):
      return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])
  
  @wrapper
  def make_lowercase(self):
      return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])
      
  @wrapper
  def capitalize_words(self):
      return " ".join([word.capitalize() for word in self.split()])
    


# In[25]:


np.version.version


# In[ ]:


class MySet(set):

  def wrapper(func):
    def inner_func(self, other):
      return MySet(func(self, other))
    return inner_func

  def is_empty(self):
        return len(self) == 0
    
  def has_duplicates(self):
        return len(self) != len(set(self))

  @wrapper
  def union_with(self, other):
        return self.union(other)
        
  @wrapper
  def intersection_with(self, other):
        return self.intersection(other)
    
  @wrapper
  def difference_with(self, other):
        return self.difference(other)


# In[ ]:


string_example = MyString("Aa Bb Cc")


# In[ ]:


type(string_example)


# In[ ]:


type(string_example.replace('A', 'F'))


# In[ ]:


print(type(string_example.reverse()))


# In[ ]:


string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})

print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))


# In[ ]:


string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})

print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))


# # Задание 4 (5 баллов)

# Напишите декоратор `switch_privacy`:
# 1. Делает все публичные **методы** класса приватными
# 2. Делает все приватные методы класса публичными
# 3. Dunder методы и защищённые методы остаются без изменений
# 4. Должен работать тестовый код ниже, в теле класса писать код нельзя
# 
# **Модули использовать нельзя**

# In[ ]:


# Ваш код здесь
class ExampleClass:
    # Но не здесь
    def public_method(self):
        return 1
    
    def _protected_method(self):
        return 2
    
    def __private_method(self):
        return 3
    
    def __dunder_method__(self):
        pass


# In[ ]:


test_object = ExampleClass()

test_object._ExampleClass__public_method()   # Публичный метод стал приватным


# In[ ]:


test_object.private_method()   # Приватный метод стал публичным


# In[ ]:


test_object._protected_method()   # Защищённый метод остался защищённым


# In[ ]:


test_object.__dunder_method__()   # Дандер метод не изменился


# In[ ]:


hasattr(test_object, "public_method"), hasattr(test_object, "private")   # Изначальные варианты изменённых методов не сохраняются


# # Задание 5 (7 баллов)

# Напишите [контекстный менеджер](https://docs.python.org/3/library/stdtypes.html#context-manager-types) `OpenFasta`
# 
# Контекстные менеджеры это специальные объекты, которые могут работать с конструкцией `with ... as ...:`. В них нет ничего сложного, для их реализации как обычно нужно только определить только пару dunder методов. Изучите этот вопрос самостоятельно
# 
# 1. Объект должен работать как обычные файлы в питоне (наследоваться не надо, здесь лучше будет использовать **композицию**), но:
#     + При итерации по объекту мы должны будем получать не строку из файла, а специальный объект `FastaRecord`. Он будет хранить в себе информацию о последовательности. Важно, **не строки, а именно последовательности**, в fasta файлах последовательность часто разбивают на много строк
#     + Нужно написать методы `read_record` и `read_records`, которые по смыслу соответствуют `readline()` и `readlines()` в обычных файлах, но они должны выдавать не строки, а объект(ы) `FastaRecord`
# 2. Конструктор должен принимать один аргумент - **путь к файлу**
# 3. Класс должен эффективно распоряжаться памятью, с расчётом на работу с очень большими файлами
#     
# Объект `FastaRecord`. Это должен быть **датакласс** (см. про примеры декораторов в соответствующей лекции) с тремя полями:
# + `seq` - последовательность
# + `id_` - ID последовательности (это то, что в фаста файле в строке, которая начинается с `>` до первого пробела. Например, >**GTD326487.1** Species anonymous 24 chromosome) 
# + `description` - то, что осталось после ID (Например, >GTD326487.1 **Species anonymous 24 chromosome**)
# 
# 
# Напишите демонстрацию работы кода с использованием всех написанных методов, обязательно добавьте файл с тестовыми данными в репозиторий (не обязательно большой)
# 
# **Можно использовать модули из стандартной библиотеки**

# In[ ]:


# Ваш код здесь


with OpenFasta(os.path.join("data", "example.fasta")) as fasta:
    # Ваш код здесь
    pass


# # Задание 6 (7 баллов)

# 1. Напишите код, который позволит получать все возможные (неуникальные) генотипы при скрещивании двух организмов. Это может быть функция или класс, что вам кажется более удобным.
# 
# Например, все возможные исходы скрещивания "Aabb" и "Aabb" (неуникальные) это
# 
# ```
# AAbb
# AAbb
# AAbb
# AAbb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# aabb
# aabb
# aabb
# aabb
# ```
# 
# 2. Напишите функцию, которая вычисляет вероятность появления определённого генотипа (его ожидаемую долю в потомстве).
# Например,
# 
# ```python
# get_offspting_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Аabb")   # 0.5
# 
# ```
# 
# 3. Напишите код, который выводит все уникальные генотипы при скрещивании `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` и `'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН'`, которые содержат в себе следующую комбинацию аллелей `'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл'`
# 4. Напишите код, который расчитывает вероятность появления генотипа `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` при скрещивании `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн` и `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн`
# 
# Важные замечания:
# 1. Порядок следования аллелей в случае гетерозигот всегда должен быть следующим: сначала большая буква, затем маленькая (вариант `AaBb` допустим, но `aAbB` быть не должно)
# 2. Подзадачи 3 и 4 могут потребовать много вычислительного времени (до 15+ минут в зависимости от железа), поэтому убедитесь, что вы хорошо протестировали написанный вами код на малых данных перед выполнением этих задач. Если ваш код работает **дольше 20 мин**, то скорее всего ваше решение не оптимально, попытайтесь что-нибудь оптимизировать. Если оптимальное решение совсем не получается, то попробуйте из входных данных во всех заданиях убрать последний ген (это должно уменьшить время выполнения примерно в 4 раза), но **за такое решение будет снято 2 балла**
# 3. Несмотря на то, что подзадания 2, 3 и 4 возможно решить математически, не прибегая к непосредственному получению всех возможных генотипов, от вас требуется именно brute-force вариант алгоритма
# 
# **Можно использовать модули из стандартной библиотеки питона**, но **за выполнение задания без использования модулей придусмотрено +3 дополнительных балла**

# In[1]:


import random 
import numpy as np 


# In[2]:


def get_alleles(genotype):  # функция разбивающая генотип на  аллели
  allels = []
  st = 0
  for i in range(2, len(genotype)+1, 2):
    allels.append(genotype[st:i])
    st += 2
  return allels


# In[3]:


def wrapper_1(uniq = False):
  def get_gametes(genotype):
    alleles = get_alleles(genotype)
    heterozig = sum(map(lambda x: 1 if len(set(x))==2 else 0, alleles))  # число гетерозигот
    gametes = set()
    while len(gametes) != 2**heterozig:  # генерируем пока не достигнем 2**heterozig гамет
      gameta = ''.join(list(map(lambda x: x[np.random.choice(2, 1).item()], alleles)))
      gametes.add(gameta)
    gametes = list(gametes)
    if not uniq:
      if len(gametes) < 2**len(alleles): # добиваем до 2**n гамет, n - кол-ов генов
        gametes *= 2**len(alleles)//len(gametes)
        return gametes
    else:
        return gametes
  return get_gametes



# In[4]:


wrapper_1(uniq = True)('AaBB')


# In[5]:


wrapper_1(uniq = False)('AaBB')


# In[6]:


def split(gamets): # ['ABC'] -> ['A', 'B', 'C']
    gamets = list(map(lambda x: list(x), gamets))
    return gamets


# In[7]:


def noneunique_offspring(parent1, parent2, func, split):
  gametes_1 = split(func(parent1))
  gametes_2 = split(func(parent2))
  offspring = []
  for i in gametes_1:
    for j in gametes_2:
      offspr = list(zip(i, j))
      offspring.append(''.join(list(map(lambda x: x[0]+x[1] if x[0].isupper() else x[1]+x[0], offspr))))
  return offspring


# In[10]:


offspring = noneunique_offspring('AaBbСС', 'AaBbСС', wrapper_1(uniq = False), split)


# In[47]:





# In[11]:


def get_offspring_genotype_probability(parent1, parent2, target_genotype, func, split, arg = wrapper_1(uniq = False)):
    offspring = func(parent1, parent2, arg, split)
    count = 0
    for i in offspring:
      if i == target_genotype:
        count += 1
    return count/(len(offspring))


# In[12]:


get_offspring_genotype_probability('Aabb', 'Aabb', 'Aabb', noneunique_offspring, split, arg = wrapper_1(uniq = False))


# In[13]:


def wrapper(func, *args, **kwargs):
  def inner_func():
    offspring = list(set(func(*args, **kwargs)))
    return offspring
  return inner_func()


# In[14]:


offspring = wrapper(noneunique_offspring, 'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн', 'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн', wrapper_1(uniq = True), split)


# In[15]:


len(offspring) == len(list(set(offspring)))  # все уникальные 


# In[ ]:


# Ваш код здесь (1 и 2 подзадание)


# In[ ]:


# Ваш код здесь (3 подзадание)


# In[ ]:


# Ваш код здесь (4 подзадание)

