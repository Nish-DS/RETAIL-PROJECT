#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


# In[2]:


Customer = pd.read_csv('F:/Python (ANALYTIX LAB)/Customer.csv')


# In[3]:


Customer.head()


# In[4]:


Customer.info()


# In[5]:


Customer.shape


# In[6]:


prod_info = pd.read_csv('F:/Python (ANALYTIX LAB)/prod_cat_info.csv')


# In[7]:


prod_info.head()


# In[8]:


prod_info.info()


# In[9]:


prod_info.shape


# In[10]:


transactions = pd.read_csv('F:/Python (ANALYTIX LAB)/Transactions.csv')


# In[11]:


transactions.head()


# In[12]:


transactions.info()


# In[13]:


transactions.shape


# In[14]:


#merging prod_info and transactions


# In[15]:


prod_trans = pd.merge(left = transactions, right = prod_info, left_on = ['prod_subcat_code', 'prod_cat_code'], 
         right_on = ['prod_sub_cat_code','prod_cat_code'], how = 'left')


# In[16]:


prod_trans.head()


# In[17]:


#merging prod_trans and Customer


# In[18]:


Customer_Final = pd.merge(left = prod_trans, right = Customer, left_on = 'cust_id', right_on = 'customer_Id', how = 'left')


# In[19]:


Customer_Final.head()


# In[20]:


Customer_Final.dtypes


# In[21]:


##Converting tran_date into Correct Data Type


# In[22]:


Customer_Final.tran_date.head()


# In[23]:


Customer_Final['tran_date'] = pd.to_datetime(Customer_Final.tran_date)


# In[24]:


Customer_Final.DOB


# In[25]:


Customer_Final['DOB'] = pd.to_datetime(Customer_Final.DOB)


# In[26]:


Customer_Final.dtypes


# In[27]:


#checking missing values


# In[28]:


Customer_Final.isna().sum()


# In[29]:


#Checking duplicates


# In[30]:


Customer_Final.duplicated().sum()


# In[31]:


Customer_Final.drop_duplicates(inplace = True)


# In[32]:


Customer_Final.duplicated().sum()


# ### Summary Report

# In[34]:


##Get the column names and their corresponding data types


# In[35]:


Customer_Final.dtypes


# In[36]:


## Top 10 observations


# In[37]:


Customer_Final.head(10)


# In[38]:


##Bottom 10 observations


# In[39]:


Customer_Final.tail(10)


# In[40]:


##“Five-number summary” for continuous variables (min, Q1, median, Q3 and max


# In[42]:


Customer_Final.describe().T


# In[43]:


## Frequency tables for all the categorical variables


# In[45]:


Customer_Final.select_dtypes(object).describe()


# In[46]:


## Generate histograms for all continuous variables and frequency bars for categorical variables.


# In[49]:


Cust_Final_Cont = Customer_Final.select_dtypes(['int64', 'float64'])


# In[52]:


Cust_Final_Cont.columns


# In[58]:


for var in Cust_Final_Cont.columns:
    Cust_Final_Cont[var].plot(kind='hist')
    plt.grid()
    plt.title(var)
    plt.show()


# In[60]:


Cust_Fin_Categ = Customer_Final.select_dtypes(object)


# In[61]:


Cust_Fin_Categ.columns


# In[62]:


for var in Cust_Fin_Categ.columns:
    sns.countplot(Cust_Fin_Categ[var])
    plt.title(var)
    plt.show()


# In[63]:


## Time period of the available transaction data


# In[65]:


max_tran_date = Customer_Final.tran_date.max()


# In[66]:


min_tran_date = Customer_Final.tran_date.min()


# In[67]:


max_tran_date


# In[68]:


min_tran_date


# In[73]:


max_tran_date - min_tran_date


# In[74]:


## Count of transactions where the total amount of transaction was negative


# In[79]:


Customer_Final[Customer_Final.total_amt < 0].transaction_id.count()


# In[80]:


## Analyze which product categories are more popular among females vs male customers.


# In[81]:


Customer_Final.head()


# In[87]:


Customer_Final.groupby(['prod_cat','Gender']).Qty.sum().reset_index().T


# In[88]:


# Product Categories which are popular among female are:
# Bags
# Footwear


# In[89]:


## Which City code has the maximum customers and what was the percentage of customers from that city?


# In[93]:


citycode_customers = Customer_Final.groupby('city_code').customer_Id.count().sort_values(ascending = False)


# In[94]:


citycode_customers


# In[95]:


citycode_customers.head(1)


# In[97]:


(citycode_customers.head(1)/citycode_customers.sum())*100


# In[98]:


## Which store type sells the maximum products by value and by quantity?


# In[102]:


storetype_max = Customer_Final.groupby('Store_type')['Rate','Qty'].sum().sort_values(by = 'Qty',ascending = False)


# In[103]:


storetype_max


# In[104]:


storetype_max.head(1)


# In[105]:


## What was the total amount earned from the "Electronics" and "Clothing" categories from Flagship Stores?


# In[106]:


Customer_Final.head()


# In[115]:


Customer_Final[(Customer_Final.prod_cat.isin(['Electronics', 'Clothing'])) & (Customer_Final.Store_type == 'Flagship store')].total_amt.sum()


# In[116]:


## What was the total amount earned from "Male" customers under the "Electronics" category?


# In[119]:


Customer_Final[(Customer_Final.Gender == 'M') & (Customer_Final.prod_cat == 'Electronics')].total_amt.sum()


# In[120]:


## How many customers have more than 10 unique transactions, after removing all transactions which have any negative amounts?


# In[122]:


Cust_Final_Positive = Customer_Final[Customer_Final.Qty > 0]


# In[125]:


Cust_Final_Positive.duplicated(keep = False)


# In[126]:


Cust_Final_Positive[Cust_Final_Positive.duplicated(keep = False)] #all records are unique


# In[133]:


unique_trans = Cust_Final_Positive.groupby(['cust_id','prod_cat','prod_subcat']).transaction_id.count()


# In[136]:


unique_trans = unique_trans.reset_index()


# In[137]:


unique_trans


# In[139]:


unique_trans_count = unique_trans.groupby('cust_id').transaction_id.count().reset_index()


# In[140]:


unique_trans_count


# In[142]:


unique_trans_count[unique_trans_count.transaction_id > 10]


# In[143]:


#There are no customers who have more than 10 unique transactions


# In[144]:


## For all customers aged between 25 - 35, find out:


# In[152]:


current_date = pd.Timestamp.now()


# In[155]:


current_date.year


# In[150]:


Customer_Final.DOB.dt.year


# In[157]:


age = current_date.year - Customer_Final.DOB.dt.year


# In[158]:


Customer_Final['Age'] = age


# In[159]:


Customer_Final.head()


# In[162]:


Cust = Customer_Final[(Customer_Final.Age >= 25) & (Customer_Final.Age <= 35)].reset_index()


# In[161]:


## What was the total amount spent for “Electronics” and “Books” product categories?


# In[165]:


Cust[Cust.prod_cat.isin(['Books','Electronics'])].total_amt.sum()


# In[166]:


## What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014


# In[167]:


Cust.head()


# In[173]:


Cust[(Cust.tran_date >= '2014-01-01') & (Cust.tran_date <= '2014-03-01')].total_amt.sum()

