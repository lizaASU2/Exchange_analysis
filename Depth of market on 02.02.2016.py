import pandas as pd
import csv
import numpy as np
from operator import itemgetter

# загружаем данные
df = pd.read_table(r'old_data_test_02.02.16_165921.txt',header=None,sep='|')
df.head()

# определяем доступные инструменты
s=[]
x = np.array (df.values)
for i in range(len(df.values)):
    s+=[df.values[i][2]]
unique_inst =sorted((list(set(s))))
print('Доступные инструменты: \n',unique_inst)

# вводим инструмент и время
inst=str(input('Введите название инструмента для сборки биржевого стакана: '))
time=str(input('Введите время сборки биржевого стакана в формате HHMMSSZZZ : '))

#Для теста
#inst='KMAZ'
#time='165621000'

#дискретные заявки на покупку
orderB=[]
#дискретные заявки на продажу
orderS=[]
# записываем данные из файла в orderB и orderS
for i in range(len(df.values)):
    if df.values[i][2]==inst:    # по необходимому инструменту
        if (df.values[i][4]<=int(time)) :   # в определенное время
            if df.values[i][6]==1:   # ранжирование по типу события: 1- пришла заявки->вносим в список
                if df.values[i][3]=='B':
                    orderB+=[df.values[i]]
                else:
                    orderS+=[df.values[i]]
            if df.values[i][6]==2:   # ранжирование по типу события: 2 - сделка->смотрим на объем
                if df.values[i][3]=='B':
                    for j in orderB:
                        if orderB[j][8]==df.values[i][8]:
                            orderB.remove(orderB[j][8])
                        if orderB[j][8]>df.values[i][8]:
                            orderB[j][8]=orderB[j][8]-df.values[i][8]
                        if orderB[j][8]<df.values[i][8]:
                            orderB.remove(orderB[j][8])                           
                if df.values[i][3]=='S':
                    for j in orderS:
                        if orderS[j][8]==df.values[i][8]:
                            orderS.remove(orderS[j][8])
                        if orderS[j][8]>df.values[i][8]:
                            orderS[j][8]=orderS[j][8]-df.values[i][8]
                        if orderS[j][8]<df.values[i][8]:
                            orderS.remove(orderS[j][8]) 
                            
#сортировка по цене
orderB=sorted(orderB,key=lambda elem: elem[7])
orderS=sorted(orderS,key=lambda elem: elem[7])
#print(orderB)
#print(orderS)

# ценовые уровни Bid(агрегированные показатели цена — объем)
OrderBookB=[]
vol=0 # объем в стакане

# выявляем уникальные цены в OrderBookB
ss=[]
xx = np.array(orderB)
for i in range(len(orderB)):
    ss+=[orderB[i][7]]
unique_priceB =sorted((list(set(ss))))

# собирем стакан под Bid
for i in range(len(unique_priceB)):
    for j in range(len(orderB)):
        if (unique_priceB[i]==orderB[j][7]):
            vol+=int(orderB[j][8])
    OrderBookB.append([unique_priceB[i],str(vol)])
    vol=0    
OrderBookB=sorted(OrderBookB,key=lambda elem: elem[0], reverse=True)

# записываем ценовые уровни Bid в файл
with open("Bid.txt", 'w') as filehandle: 
    filehandle.write('Инструмент:'+inst+' \n')
    filehandle.write('Время:'+time+' \n')
    filehandle.write('Bid        Size \n')
    for listitem in OrderBookB:
        filehandle.write('%s\n' % listitem)

# ценовые уровни Ask(агрегированные показатели цена — объем)
OrderBookS=[]
vol1=0

# выявляем уникальные цены в OrderBookB
sss=[]
xxx = np.array(orderS)
for i in range(len(orderS)):
    sss+=[orderS[i][7]]
unique_priceS =sorted((list(set(sss))))

# собирем стакан под Ask
for i in range(len(unique_priceS)):
    for j in range(len(orderS)):
        if (unique_priceS[i]==orderS[j][7]):
            vol1+=int(orderS[j][8])
    OrderBookS.append([unique_priceS[i],str(vol1)])
    vol1=0
# записываем ценовые уровни Ask в файл
with open("Ask.txt", 'w') as filehandle: 
    filehandle.write('Инструмент:'+inst+' \n')
    filehandle.write('Время:'+time+' \n')
    filehandle.write('Ask        Size \n')
    for listitem in OrderBookS:
        filehandle.write('%s\n' % listitem)

