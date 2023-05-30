#!/usr/bin/env python
# coding: utf-8

# In[160]:


#IMPORTING THE DATA CLEANING LIBRARIES FOR PYTHON
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
#Loading the dataset to be cleaned
fifa_data =  pd.read_csv("C:/Users/ayoki/OneDrive/Desktop/fifa21 raw data v2.csv", low_memory = False)
fifa_data.head(5)


# In[161]:


#GETTING INFORMATION ON THE DATASET
fifa_data.info()


# In[162]:


#Finding the unique values in the name colum
fifa_data.Name.unique()


# In[163]:


#Renaming the column LongName as GovernmentName
fifa = fifa_data.rename(columns={'LongName':'GovernmentName'})


# In[164]:


#DROPPING SOME COLUMNS IN THE DATASET
fifa.drop(fifa.columns [[3,4,18]],axis = 1,inplace = True)
fifa


# In[165]:


#When I do df.isnull().sum(), I get the count of null values in a column
fifa.isnull().sum()


# In[166]:


#The Hits column has some null values so we fill it up with zeros and we simply cannot drop the column in this analysis
fifa.Hits = fifa.Hits.fillna('0')
fifa.info()


# In[167]:


#WORKING ON THE JOINED COLUMN
from datetime import datetime
fifa['Joined']


# In[168]:


#using function 'replace_date_column' and datetime to seperate one column into three 
def replace_date_column(fifa, Joined):
    fifa = fifa.assign(Year=pd.to_datetime(fifa[Joined]).dt.year,
                   Month=pd.to_datetime(fifa[Joined]).dt.month,
                   Day=pd.to_datetime(fifa[Joined]).dt.day)
    fifa.drop(columns=[Joined], inplace=True)
    return fifa


# In[169]:


fifa = replace_date_column(fifa, 'Joined')
print(fifa)


# In[170]:


fifa.info()


# In[171]:


#TO ENSURE CONSISTENCY IN NAMING, OVA IS REMANED
fifa = fifa.rename(columns = {'↓OVA': 'OVA'})
#Cleaning up the club dataset
fifa['Club']= fifa['Club'].str.replace('\n\n\n\n','')
fifa.tail(6)


# In[172]:


#The next Column to clean is the contract. list of unique contracts
fifa.Contract.unique()


# In[173]:


# define a function to change the values with 'on loan' as an "On loan" category
# define the players with active loans as Active and they can be located easily cause they contain '~'
def contract(a):
    if "On Loan" in a:
        a = 'ON LOAN'
        return a
    elif '~' in a:
        a = 'ACTIVE'
        return a
    elif 'Free' in a:
        a = "FREE"
        return a


# In[174]:


fifa.Contract = fifa.Contract.apply(contract)
fifa.Contract = fifa.Contract.astype('category')
# Rename the column to Contract status
fifa = fifa.rename(columns={'Contract':'ContractStatus'})
fifa.head()


# In[175]:


#The next step is to clean the Height and Weight columns as they are both cast as an object type
fifa.Height.unique()
#from the data, we have "cm" and also 'feet/inches'


# In[176]:


def convert_height(x):
    if x[-1] == '"':
        x = x.replace("\"","") # Remove the inch symbol (")
        inch = int(x[2:]) * 2.54 # Convert inches to centimeters
        foot = int(x[0]) * 30.48  # Convert feet to centimeters
        return round(foot+inch) # Return the total height in centimeters
    elif x[-1] == "m":
        return int(x[:-2])  # Remove the "m" symbol and return the height in centimeters


# In[177]:


fifa.Height = fifa.Height.apply(convert_height)
fifa.Height.unique()


# In[ ]:




