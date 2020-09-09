#!/usr/bin/env python
# coding: utf-8

# In[16]:


from datetime import date
from datetime import datetime
from datetime import date
import numpy as np
import pandas as pd
#读取文件
data=pd.read_csv(r"E:\python\flightprice\携程机票.csv")
data.head()


# In[5]:


#获取日期标记
a=[0 for x in range(len(data['departureDate']))]
for i in range(len(data['departureDate'])):
    a[i]=data['departureDate'][i][:10]
data['date']=a
#data.head(3000)


# In[19]:


#转换departureDate数据类型
data['departureDate']=pd.to_datetime(data['departureDate'])
data['arrivalDate']=pd.to_datetime(data['arrivalDate'])
data['date']=pd.to_datetime(data['date'])

data.dtypes
#data.dtypesfrom datetime import date
#from datetime import datetime


# In[7]:


data.to_csv(r"E:\python\flightprice\携程.csv",index=0)


# In[31]:


#划分时间段
from datetime import date
from datetime import datetime

time1 = datetime.strptime('00:00','%H:%M').time()
time2 = datetime.strptime('04:00','%H:%M').time()
time3 = datetime.strptime('08:00','%H:%M').time()
time4 = datetime.strptime('12:00','%H:%M').time()
time5 = datetime.strptime('16:00','%H:%M').time()
time6 = datetime.strptime('20:00','%H:%M').time()
time7 = datetime.strptime('23:59','%H:%M').time()
df1=data[(data.departureDate.dt.time >= time1)&(data.departureDate.dt.time < time2)]
df2=data[(data.departureDate.dt.time >= time2)&(data.departureDate.dt.time < time3)]
df3=data[(data.departureDate.dt.time >= time3)&(data.departureDate.dt.time < time4)]
df4=data[(data.departureDate.dt.time >= time4)&(data.departureDate.dt.time < time5)]
df5=data[(data.departureDate.dt.time >= time5)&(data.departureDate.dt.time < time6)]
df6=data[(data.departureDate.dt.time >= time6)&(data.departureDate.dt.time < time7)]
#存入时间段标记
a=[0 for x in range(len(data['departureDate']))]
for i in df1.index:
    a[i]='0-4'
for i in df2.index:
    a[i]='4-8'
for i in df3.index:
    a[i]='8-12'
for i in df4.index:
    a[i]='12-16'
for i in df5.index:
    a[i]='16-20'
for i in df6.index:
    a[i]='20-24'
#print(df1.index[0])
data['timeId']=a
data.head(2000)


# In[29]:


data.head(2000)


# In[10]:


data.to_csv(r"E:\python\flightprice\携程机票.csv",index=0)


# In[32]:


import seaborn as sns
df=data[(data['departureCityName']=="上海")&(data['arrivalCityName']=="北京")]
plo=sns.relplot(x="timeId", y="price", data=df,
            hue="airlineName", #style="品号", 
            col="date", col_wrap=1,
            markers=True,dashes=False,# 添加标记，禁止虚线
            kind="line",
            height=7,aspect=1.75)


# In[35]:


import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei',font_scale=1.5)  # 解决Seaborn中文显示问题并调整字体大小
df1=data[(data['departureCityName']=="上海")&(data['arrivalCityName']=="北京")]
plo=sns.relplot(x="date", y="price", data=df1,
            hue="flightNumber", #style="品号", 
            col="airlineName", col_wrap=1,
            markers=True,dashes=False,# 添加标记，禁止虚线
            kind="line",
            height=7,aspect=1.75)


# In[43]:


df=data.loc[:,'airlineName'].value_counts()
df.index


# In[53]:


plt.pie(df, explode=None, labels=None,  
    colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'),  
    autopct=None, pctdistance=0.6, shadow=False,  
    labeldistance=1.1, startangle=None, radius=None,  
    counterclock=True, wedgeprops=None, textprops=None,  
    center = (0, 0), frame = False )  


# In[54]:


plt.pie(df, labels=df.index, autopct='%2.2f%%')
plt.axis('equal') 


# In[ ]:




