#!/usr/bin/env python
# coding: utf-8

# Задание 1. Работа с реальными данными (20 баллов)

# In[174]:


path_bed  = './alignment.bed'
path_gff = './rrna_annotation.gff'


# In[175]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


# In[236]:





# In[176]:


colnames_gff = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
colnames_bed = ["chrom", "chromStart", "chromEnd", "name", "score", "strand"]


# In[177]:


alignment_bed = pd.read_csv(path_bed, sep = "\t", names = colnames_bed)


# In[178]:


alignment_bed.head()


# In[179]:


gff = pd.read_csv(path_gff, sep = "\t", skiprows=1, names = colnames_gff)


# In[180]:


def search_RNA(string):
    res = re.findall('\d{1,2}S', string)
    return res[0]


# In[181]:


gff.attributes = gff.attributes.map(lambda p: search_RNA(p))


# In[182]:


gff.groupby(["seqid"]).attributes.apply(lambda x: x)


# In[183]:


gff


# 

# In[184]:


gff.shape


# In[185]:


gff["counter"] = pd.Series([0] * 348)


# In[186]:


gff


# In[187]:


count_rna = gff.groupby(["seqid", "attributes"]).counter.apply(lambda x: x.count())   # немного некрасиво работает метод, но инфу получил


# In[188]:


type(count_rna.index)   # мультииндекс
count_rna = count_rna.to_dict()


# In[188]:





# In[189]:


check = {"16S": "5S", "23S": "16S", "5S":"23S"}
all_rna = []
ref = []
value = []
for key in count_rna:
    all_rna.append(key[1])
    ref.append(key[0])
    value.append(count_rna[key])


# In[190]:


rna = ["5S", "16S", "23S"]
all_comb = []
for i in ref:
    for k in rna:
        all_comb.append((i, k))


# In[191]:


rest = set(all_comb) - set(count_rna.keys())


# In[192]:


rest = list(rest)


# In[193]:


rest


# In[194]:


count_rna[rest[0]] = 0
count_rna[rest[1]] = 0


# In[197]:


ref = []
for key in count_rna:
    ref.append(key[0])


# In[198]:


new_ref = {}
for i in set(ref):
    new_ref[i] = {}
    for key in count_rna:
        if key[0] == i:
            new_ref[i][key[1]] = count_rna[key]


# In[199]:


new_ref


# In[200]:


rna_5S = []
rna_23S = []
rna_16S = []
for key in new_ref:
    rna_5S.append(new_ref[key]['5S'])
    rna_23S.append(new_ref[key]['23S'])
    rna_16S.append(new_ref[key]['16S'])


# In[170]:


len(rna_23S) == len(rna_23S) == len(rna_16S)


# In[201]:



N = len(rna_23S)
ind = np.arange(N)
width = 0.25

xvals = rna_5S
bar1 = plt.bar(ind, xvals, width, color = 'r')

yvals = rna_23S
bar2 = plt.bar(ind+width, yvals, width, color='g')

zvals = rna_16S
bar3 = plt.bar(ind+width*2, zvals, width, color = 'b')

plt.xlabel("Sequence")
plt.ylabel('Count')

plt.xticks(ind+width, list(new_ref.keys()), rotation='vertical')
plt.legend( (bar1, bar2, bar3), ('5S', '23S', '16S') )
plt.show()



# In[202]:


gff.drop("counter", axis=1, inplace=True)


# In[203]:


any(gff.duplicated())   # нет дубликатов


# In[204]:


alignment_bed = alignment_bed.rename(columns = {"chrom": "seqid"})


# In[205]:


alignment_bed


# In[206]:


df = pd.merge(gff, alignment_bed, on='seqid')   # объединяем по совпадениям референсных геномов, иначе точно не совпадают, далее будем считать границу


# In[207]:


idx = np.where((df.chromEnd >= df.end) & (df.chromStart <= df.start)) #считаю границу, берем индексы прошедших условие
idx = idx[0].tolist()
df = df.iloc[idx]


# In[208]:


df = df.drop(df.columns[[-1, -2]], axis = 1)


# In[235]:


df.head()   #итогове пересечение контигов на сборку


# Pie chart (Доп)

# In[210]:


data_pie = pd.read_csv("Air_Traffic_Passenger_Statistics.csv")


# In[211]:


idx = np.where(data_pie["Published Airline"].value_counts() >= 100)[0].tolist()


# In[212]:


slice = data_pie["Published Airline"].iloc[idx].value_counts()
labels = data_pie["Published Airline"].iloc[idx].value_counts().index


# In[213]:


explode = [0] * len(labels)
explode[0] = 0.1


# In[214]:


explode


# In[215]:


data_pie[data_pie["Published Airline"] == "Alaska Airlines"]["GEO Region"].value_counts().tolist()


# In[218]:


plt.pie(slice, labels = labels, explode = explode, wedgeprops= {"edgecolor": "black"}, shadow = True)
plt.title("My Awesome pie chart")
plt.tight_layout()
plt.show()


# In[221]:


geo = data_pie[data_pie["Published Airline"] == "Alaska Airlines"]["GEO Region"].value_counts().tolist()


# In[225]:


data_pie[data_pie["Published Airline"] == "Alaska Airlines"]["GEO Region"].value_counts()


# In[ ]:





# In[234]:


import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np

# make figure and assign axis objects
fig = plt.figure(figsize=(9, 5.0625))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0)

# pie chart parameters
slice = data_pie["Published Airline"].iloc[idx].value_counts()
labels = data_pie["Published Airline"].iloc[idx].value_counts().index
explode = [0] * len(labels)
explode[0] = 0.1
# rotate so that first wedge is split by the x-axis
angle = -180 * slice[0]
ax1.pie(slice, autopct='%1.1f%%', startangle=angle,
        labels=labels, explode=explode)

# bar chart parameters

xpos = 0
bottom = 0
geo = data_pie[data_pie["Published Airline"] == "Alaska Airlines"]["GEO Region"].value_counts().tolist()
width = .2
colors = [[.1, .3, .5], [.1, .3, .3], [.1, .3, .7]]

for j in range(len(geo)):
    height = geo[j]
    ax2.bar(xpos, height, width, bottom=bottom, color=colors[j])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
             ha='center')

ax2.set_title('GEO Region')
ax2.legend(('Us', 'Mexico', 'Canada'))
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
# get the wedge data
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r
bar_height = sum([item.get_height() for item in ax2.patches])

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
                      coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)


x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
                      coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show();


# |Eda

# In[3]:


covid = pd.read_csv("./owid-covid-data.csv")


# In[4]:


covid.columns


# In[5]:


import numpy as np


# In[6]:


covid.head()


# In[13]:


covid


# In[22]:





# In[20]:





# In[22]:


NAN = pd.DataFrame(NAN, columns=["column_name", "percentage"])
NAN


# In[7]:


#посмотрим total deaths по странам


# In[45]:


labels = covid.groupby(["continent"]).total_deaths.agg(["count"]).index
slice = covid.groupby(["continent"]).total_deaths.agg(["count"])["count"].tolist()


# In[48]:


plt.pie(slice, labels = labels, wedgeprops= {"edgecolor": "black"}, shadow = True)
plt.title("Occurance by continent")
plt.tight_layout()
plt.show()


# In[66]:


#далее посмотрим на распределение смертей по самым большим сегментам - Европы и Африки


# In[56]:


Europe = covid.query("continent == 'Europe'")
labels = Europe.groupby(["location"]).total_deaths.agg(["count"]).index
counter = Europe.groupby(["location"]).total_deaths.agg(["count"])["count"].tolist()


# In[64]:





# In[64]:


fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(labels, counter);


# In[65]:


Africa = covid.query("continent == 'Africa'")
labels = Africa.groupby(["location"]).total_deaths.agg(["count"]).index
counter = Africa.groupby(["location"]).total_deaths.agg(["count"])["count"].tolist()
fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(labels, counter);


# In[ ]:





# Распределение больше похоже к равномерному

# In[69]:


get_ipython().system('pip install plotly')


# In[70]:


import plotly.graph_objects as go


# In[72]:


covid.columns


# In[79]:


# посмотрим как коррелируют общее число вакцинировавших и число новых случаев заболевания


# In[110]:


vacc = covid.people_fully_vaccinated[covid.people_fully_vaccinated.notna() == True].sort_values()
new_case = covid.new_cases.iloc[vacc.index]
plt.scatter(vacc, new_case, c ="blue")
plt.show()


# In[111]:


covid.columns


# In[113]:


vacc = covid.total_vaccinations[covid.total_vaccinations.notna() == True].sort_values()
new_case = covid.new_cases.iloc[vacc.index]
plt.scatter(vacc, new_case, c ="green")
plt.show()


# In[109]:


# ожидали увидеть антикорреляцию, но не всех точках данные коррелируют


# Выделим топ 10 стран по кол-ву смертей

# In[151]:


covid.location


# In[122]:


deaths_per_country = covid.groupby(["location"]).total_deaths.agg(["count"]).reset_index().sort_values(("count"), ascending = False)


# In[129]:


deaths_per_country.index = np.arange(244)


# In[138]:


deaths_per_country.iloc[np.arange(10)] #странные страны, ну ладно


# In[146]:


people_vaccinated_per_100 = covid.people_vaccinated_per_hundred[covid.people_vaccinated_per_hundred.notna()]


# In[154]:


people_vaccinated_per_100 = people_vaccinated_per_100.sort_values(ascending = False).head(n = 10)


# In[160]:


set(covid.location.iloc[people_vaccinated_per_100.index].tolist())


# In[147]:


people_vaccinated_per_100.index


# In[139]:


total_vac = covid.groupby(["location"]).total_vaccinations.agg(["count"]).reset_index().sort_values(("count"), ascending = False)


# In[140]:


total_vac


# Violin plot

# In[1]:


path_data = "./diffexpr_data.tsv"


# In[5]:


diffexpr = pd.read_csv(path_data, sep = "\t")


# In[6]:


diffexpr


# In[ ]:




