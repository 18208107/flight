#!/usr/bin/env python
# coding: utf-8

# In[40]:


from datetime import date
from datetime import datetime
from datetime import date
import numpy as np
import pandas as pd


# In[41]:


#获取日期标记
def get_date(data):
    a=[0 for x in range(len(data['departureDate']))]
    for i in range(len(data['departureDate'])):
        a[i]=data['departureDate'][i][:10]
        data['date']=a  
    return data


# In[46]:


#划分时间段
def timecut(data):
    data['departureDate']=pd.to_datetime(data['departureDate'])
    data['arrivalDate']=pd.to_datetime(data['arrivalDate'])
    data['date']=pd.to_datetime(data['date'])
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
    return data


# In[44]:


if __name__ == "__main__":
    #读取文件
    df=pd.read_csv(r"E:\python\flightprice\flightprice.csv",encoding="gbk")
    #转换departureDate数据类型
    df['departureDate']=pd.to_datetime(df['departureDate'])
    df['arrivalDate']=pd.to_datetime(df['arrivalDate'])
    #另存新文件
    df.to_csv(r"E:\python\flightprice\携程.csv",index=0)
    #读取文件
    df=pd.read_csv(r"E:\python\flightprice\携程.csv")
    #获取日期标记
    data=get_date(df)
    #获取timeId
    df=timecut(data)
    info= df['flightlins']=data['departureCityName']+'-'+data['arrivalCityName']
    data.to_csv(r"E:\python\flightprice\携程机票.csv")

    


# In[45]:





# In[ ]:




