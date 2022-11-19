#!/usr/bin/env python
# coding: utf-8

# ### Задание 1. Работа с реальными данными (20 баллов)

# In[1]:


path_bed  = './alignment.bed'
path_gff = './rrna_annotation.gff'


# In[26]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


# In[3]:


colnames_gff = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
colnames_bed = ["chrom", "chromStart", "chromEnd", "name", "score", "strand"]


# In[4]:


alignment_bed = pd.read_csv(path_bed, sep = "\t", names = colnames_bed)


# In[5]:


alignment_bed.head()


# In[6]:


gff = pd.read_csv(path_gff, sep = "\t", skiprows=1, names = colnames_gff)


# In[7]:


def search_RNA(string):
    res = re.findall('\d{1,2}S', string)
    return res[0]


# In[8]:


gff.attributes = gff.attributes.map(lambda p: search_RNA(p))


# In[9]:


gff.groupby(["seqid"]).attributes.apply(lambda x: x)


# In[10]:


gff


# 

# In[11]:


gff.shape


# In[12]:


gff["counter"] = pd.Series([0] * 348)


# In[13]:


gff


# In[14]:


count_rna = gff.groupby(["seqid", "attributes"]).counter.apply(lambda x: x.count())   # немного некрасиво работает метод, но инфу получил


# In[15]:


type(count_rna.index)   # мультииндекс
count_rna = count_rna.to_dict()


# In[15]:





# In[16]:


check = {"16S": "5S", "23S": "16S", "5S":"23S"}
all_rna = []
ref = []
value = []
for key in count_rna:
    all_rna.append(key[1])
    ref.append(key[0])
    value.append(count_rna[key])


# In[17]:


rna = ["5S", "16S", "23S"]
all_comb = []
for i in ref:
    for k in rna:
        all_comb.append((i, k))


# In[18]:


rest = set(all_comb) - set(count_rna.keys())


# In[19]:


rest = list(rest)


# In[20]:


rest


# In[21]:


count_rna[rest[0]] = 0
count_rna[rest[1]] = 0


# In[22]:


ref = []
for key in count_rna:
    ref.append(key[0])


# In[23]:


new_ref = {}
for i in set(ref):
    new_ref[i] = {}
    for key in count_rna:
        if key[0] == i:
            new_ref[i][key[1]] = count_rna[key]


# In[24]:


new_ref


# In[25]:


rna_5S = []
rna_23S = []
rna_16S = []
for key in new_ref:
    rna_5S.append(new_ref[key]['5S'])
    rna_23S.append(new_ref[key]['23S'])
    rna_16S.append(new_ref[key]['16S'])


# In[26]:


len(rna_23S) == len(rna_23S) == len(rna_16S)


# In[27]:



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



# In[28]:


gff.drop("counter", axis=1, inplace=True)


# In[53]:


any(gff.duplicated())   # нет дубликатов


# In[30]:


alignment_bed = alignment_bed.rename(columns = {"chrom": "seqid"})


# In[31]:


alignment_bed


# In[32]:


df = pd.merge(gff, alignment_bed, on='seqid')   # объединяем по совпадениям референсных геномов, иначе точно не совпадают, далее будем считать границу


# In[33]:


idx = np.where((df.chromEnd >= df.end) & (df.chromStart <= df.start)) #считаю границу, берем индексы прошедших условие
idx = idx[0].tolist()
df = df.iloc[idx]


# In[34]:


df = df.drop(df.columns[[-1, -2]], axis = 1)


# In[38]:


df.head() #итогове пересечение контигов на сборку


# ### Задание 2. Кастомизация графиков

# In[39]:


get_ipython().system('ls')


# In[48]:


data = pd.read_csv('./diffexpr_data.tsv', sep = '\t')


# In[51]:


data.columns


# In[54]:





# In[56]:


plt.plot(figsize = (9, 10))
ax = sns.scatterplot(data = data, x = 'logFC', y = 'log_pval')


# In[ ]:





# In[ ]:





# #### Pie chart (Доп)

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


# # Eda

# In[173]:


covid = pd.read_csv("./owid-covid-data.csv")


# In[173]:





# In[174]:


import numpy as np


# In[175]:


covid.head()


# In[5]:


# NAN = pd.DataFrame(NAN, columns=["column_name", "percentage"])
# NAN


# In[6]:


#посмотрим total deaths по странам


# In[7]:


labels = covid.groupby(["continent"]).total_deaths.agg(["count"]).index
slice = covid.groupby(["continent"]).total_deaths.agg(["count"])["count"].tolist()


# In[8]:


plt.pie(slice, labels = labels, wedgeprops= {"edgecolor": "black"}, shadow = True)
plt.title("Occurance by continent")
plt.tight_layout()
plt.show()


# ##### далее посмотрим на распределение смертей по самым большим сегментам - Европы и Африки

# In[9]:


Europe = covid.query("continent == 'Europe'")
labels = Europe.groupby(["location"]).total_deaths.agg(["count"]).index
counter = Europe.groupby(["location"]).total_deaths.agg(["count"])["count"].tolist()


# In[9]:





# In[10]:


fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(labels, counter);


# In[11]:


Africa = covid.query("continent == 'Africa'")
labels = Africa.groupby(["location"]).total_deaths.agg(["count"]).index
counter = Africa.groupby(["location"]).total_deaths.agg(["count"])["count"].tolist()
fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(labels, counter);


# In[11]:





# Распределение больше похоже к равномерному

# In[12]:


covid.columns


# ### посмотрим как (анти)коррелируют общее число вакцинировавших и число новых случаев заболевания

# In[19]:


vacc = covid.people_fully_vaccinated[covid.people_fully_vaccinated.notna() == True].sort_values()
new_case = covid.new_cases.iloc[vacc.index]
plt.scatter(vacc, new_case, c ="blue")
plt.show()


# In[20]:


covid.columns


# In[21]:


vacc = covid.total_vaccinations[covid.total_vaccinations.notna() == True].sort_values()
new_case = covid.new_cases.iloc[vacc.index]
plt.scatter(vacc, new_case, c ="green")
plt.show()


# In[22]:


# ожидали увидеть антикорреляцию, но не всех точках данные коррелируют


# ###### Выделим топ 10 стран по наименьшему кол-ву смертей и посмотрим как у них дела в вакцинацией.

# In[32]:


covid.head()


# In[116]:


deaths_per_country = covid.groupby(["location"]).total_deaths.agg(["count"]).reset_index().sort_values(("count"), ascending = True)


# In[117]:


location_low_deaths = deaths_per_country[deaths_per_country['count'] >  0]['location'].head(n=12).tolist()    #взяли страны с самым маленьким кол-ом общих смертей (с нулем не учитывали)


# In[118]:


location_low_deaths


# In[119]:


deaths_per_country = covid.groupby(["location"]).total_deaths.agg(["count"]).reset_index().sort_values(("count"), ascending = False)


# In[120]:


location_high_deaths = deaths_per_country['location'].head(n=20).tolist()


# In[121]:


location_high_deaths    #есть не страны, а целые континенты, удалим их


# In[122]:


remove = ['World', 'Europe', 'Lower middle income', 'European Union', 'International', 'North America', 'Upper middle income', 'Asia']
location_high_deaths = [i for i in location_high_deaths if i not in remove]


# In[153]:


len(location_high_deaths)


# In[154]:


sel_df = covid[covid.location.isin(location_high_deaths+location_low_deaths)]


# In[155]:


def type_deaths(row):
    if row.location in location_high_deaths:
        return 'High deaths'
    else:
        return 'low deaths'


# In[156]:


sel_df['type_country'] = sel_df.apply(type_deaths, axis = 1)


# In[164]:


sel_df = sel_df[sel_df['people_fully_vaccinated_per_hundred'].isna() == False]


# In[166]:


sel_df


# In[168]:


plt.figure(figsize = (10, 7))
ax = sns.histplot(data=sel_df, x='total_vaccinations_per_hundred', hue = 'type_country')


# Да, непонятная картина, в странах с большим кол-вом смертей больше частота вакцинированных на 100 человек тоже больше , значит картина сложнее

# In[ ]:





# In[177]:


covid.columns


# ######    влияние частоты случаев на частоту смертей

# In[205]:


def func(x):
    if x == True:
        return 'Older'
    else:
        return 'Younger'


# In[206]:


bool_ser = covid['aged_70_older'] > covid.aged_70_older.median()


# In[207]:


bool_ser.map(func)


# In[209]:


new_df = covid


# In[209]:





# In[210]:


new_df['age'] = bool_ser.map(func)


# In[211]:


sns.scatterplot(x=new_df['total_cases'], y=new_df['total_deaths'])


# ##### прослеживается  положительная корреляция, что наверное логично - большее кол-во случаев порадения провоцирует больше смертей

# In[213]:


sns.scatterplot(x=new_df['people_fully_vaccinated_per_hundred'], y=new_df['new_cases'], hue = new_df['age'])


# ##### видно что у пожилых  людей больше новых случаев , при меньшем кол-ве полностью вакцинированных людей

# ##### посмотрим на влияние кол-ва понлностью вакц людей на кол-во новых смертей

# In[218]:


sns.scatterplot(x=new_df['people_fully_vaccinated_per_hundred'], y=new_df['new_deaths'])


# ###### Видна антикорреляция, видимо как-то кол-во полностью вакцинированных людей предотвращает кол-во новых смертей

# In[219]:


sns.scatterplot(x=new_df['people_fully_vaccinated_per_hundred'], y=new_df['new_deaths'], hue = new_df['age'])


# ##### видно что у пожилых  людей больше смертей, при меньшем кол-ве полностью вакцинированных людей

# ### Violin plot

# In[101]:


path_data = "./diffexpr_data.tsv"


# In[102]:


diff_expr = pd.read_csv(path_data, sep ="\t")


# In[103]:


diff_expr.head()


# In[286]:





# КАкой выбрать порог ошибки первого рода (альфа) после поправки?
# -np.log10(0.89) - примерно 0.05
# 

# In[153]:


treshold_pval = -np.log10(0.89)
treshold_logFC = 0
stats = []
for log_VC, pval in zip(diff_expr.logFC, diff_expr.pval):
    if log_VC >= treshold_logFC and pval < treshold_pval:
        stats.append('Significantly upregulated')
    elif log_VC < treshold_logFC and pval < treshold_pval:
        stats.append('Significantly downregulated')
    elif log_VC < treshold_logFC and pval >= treshold_pval:
        stats.append('None-significantly downregulated')
    elif log_VC >= treshold_logFC and pval >= treshold_pval:
        stats.append('None-significantly upregulated')


# In[287]:


diff_expr['stat'] = pd.Series(stats)


# In[ ]:


def func(row):
    if row == True


# In[136]:


idx = np.where(diff_expr['logFC'] < 0)[0]


# In[138]:


diff_expr['logFC'].iloc[idx].min()


# In[154]:





# In[155]:


diff_expr['stat'].unique()


# In[120]:


diff_expr['stat'].value_counts()


# In[93]:


diff_expr['pval'].min()


# In[68]:


diff_expr['pval'] <= 1.3


# In[92]:





# In[62]:


sns.histplot(diff_expr['pval']);


# In[55]:


np.log10(0.05)


# In[51]:


diff_expr['stat'][diff_expr['stat'] == 'None-significantly downregulated'].index


# In[54]:


diff_expr['pval'][diff_expr['stat'] == 'Significantly downregulated']


# In[53]:


diff_expr['pval'][diff_expr['stat'] == 'None-significantly downregulated']


# In[95]:


diff_expr.head()


# 

# In[ ]:


top_signific_downregul = diff_expr[diff_expr['stat'] == 'Significantly downregulated'].sort_values(['logFC']).head(n=2)[['Sample', 'logFC', 'pval']]
top_signific_upregul = diff_expr[diff_expr['stat'] == 'Significantly upregulated'].sort_values(['logFC'], ascending=False).head(n=2)[['Sample', 'logFC', 'pval']]
df_merged = top_signific_upregul.append(top_signific_downregul, ignore_index=True)
gene_1, gene_2, gene_3, gene_4 = df_merged.Sample.tolist()
x1, x2, x3, x4 = df_merged.logFC.tolist()
y1, y2, y3, y4 = df_merged.pval.tolist()


# In[284]:


plt.figure(figsize = (10, 7))
ax = sns.scatterplot(data = diff_expr, x ='logFC', y ='log_pval', hue = 'stat', sizes=(0.5, 100))
ax.axvline(0, c = 'k', lw = 0.5, ls = '--')
ax.axhline(-np.log10(0.89), c = 'k', lw = 0.5, ls = '--')
plt.annotate(text = gene_1, xy = (x1, y1), xytext=(x1, y1), arrowprops =dict(facecolor='red'))
plt.annotate(text = gene_2, xy = (x2, y2), xytext=(x2, y2), arrowprops =dict(facecolor='red'))
plt.annotate(text = gene_3, xy = (x3, y3), xytext=(x3, y3), arrowprops =dict(facecolor='red'))
plt.annotate(text = gene_4, xy = (x4, y4), xytext=(x4, y4), arrowprops =dict(facecolor='red'))

plt.show()


# я не очень понимаю почему я не вижу none-significantly точки, почему не сохраняется масштаб относительно порога альфа который я задал
# 

# In[ ]:




