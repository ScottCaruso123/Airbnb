#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt#Matplotlib for plotting graphs and its numerical processes
import seaborn as sns # data visualization based on omatplotlib, high-level interface
import folium #allows us to map with leaflet
from folium.plugins import MarkerCluster
from folium import plugins
from folium.plugins import FastMarkerCluster
from folium.plugins import HeatMap
from scipy.stats import pearsonr


# In[2]:


#Using pandas to upload from our data source, csv file


data = pd.read_csv("AB_NYC_2019.csv", encoding='ISO-8859-1')


# In[3]:


#Getting a brief view of the data  

data.head(20)


# In[4]:


#LNow for a more clear view of our data

print('\nRows : ', data.shape[0])
print('\nColumns : ',data.shape[1])
print('\nColumns : ',data.columns.to_list())
print('\nUnique:\n', data.nunique())


# In[5]:


#Now we will check for any null or any missing values in our data set


data.isnull().sum().sort_values(ascending=False)

#Top missing data: reviews_per_month and last_review = 10052, host_name = 21, name = 16


# In[6]:


#If you wnated to drop all null values you would be dropping a little over 10,000 data points 
# cleaned_data = data.dropna()
# cleaned_data.shape


# or we can replace the name and host_name so we can
#keep 10,000 data points to give us a more accurate report

# replace_name = "&"
# replace_host_name = "%"

# data['name'].fillna(replace_name,inplace=True)
# data['host_name'].fillna(replace_host_name, inplace=True)
# data.isnull().sum().sort_values(ascending=False)

#Now we can drop the columns reviews per month and last_review
data.drop(['last_review'], axis=1, inplace=True)
data.drop(['reviews_per_month'], axis=1, inplace=True)

data.describe()


# In[7]:


#Retrieving rows based on index label

data.loc[0]


# In[8]:


#Getting a summary what of our data looks like 
data.info(verbose=True)


# ##Now let us begin our analysis

# In[9]:


#Lets begin the analysis by looking at the different types of rooms and how many there are.

data['room_type'].value_counts()


# In[10]:


#Creating a 

room_bar_chart = sns.countplot(x='room_type', order = data.room_type.value_counts().index,data=data)

#adding title and labels
room_bar_chart.set(xlabel='Room Types', ylabel='', title='Bar Chart for Room Type')


# ##Now lets take a look at the different types of neighbourhood

# In[11]:


# Percentage of neighbourhood groups

data.neighbourhood_group.value_counts(dropna = False, normalize = True)



# In[12]:


#Creating the pie chart to display different percentages of most preferred neighbourhood groups

labels = data.neighbourhood_group.value_counts().index #Creating chart's labels
sizes = data.neighbourhood_group.value_counts().values # total for each neighbourhood group
explode = (0.1, 0.2, 0.3, 0.4, 0.6)#How much space each section of the graph will have between each other

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                   shadow=True, startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set(title="Most Rented Neighbourhood Group Pie Plot")
ax.legend(wedges, labels,
          title="Neighbourhood Groups",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=8, weight="bold")
plt.show()


# ##Determining which neighbourhood in each neighbourhood group is the most preferred. 

# In[13]:


#Creating abar chart for each negihbourhood groups to show most preferred for each


sns.set(style='white', context='talk')

f, subplots = plt.subplots(len(data.neighbourhood_group.unique()), 1, figsize=(65,45))

for i, neighbourhood_group in enumerate(data.neighbourhood_group.unique()):
    neighbourhoods = data.neighbourhood[data.neighbourhood_group == neighbourhood_group]
    ax = subplots[i]
    x = np.array(neighbourhoods.value_counts().index)
    y = neighbourhoods.value_counts().values
    sns.barplot(x=x,y=y, palette='rocket', ax=ax)
    ax.axhline(0, color='k', clip_on=False)
    ax.set_ylabel(neighbourhood_group)
    
sns.despine(bottom=True)
f.suptitle('Neighourhood Groups by Neighbourhoods')
plt.setp(f.axes, yticks=[])
plt.tight_layout(h_pad=2)
plt.show()





#The following graphs show that the most popular areas to stay are:
    #Brooklyn(Williamsburg)
    #Manhattan(Harlem)
    #Queens(Astoria)
    #Staten ISland(St.George)
    #Bronx(Kingsbridge)
    


# In[14]:


#Violin [plot to show density 

sns.set(style='whitegrid')

min_price = 1000
#Airbnb prices 
data_price= data[data.price < min_price]

#Set up the matplot figure 
fig, ax = plt.subplots(figsize=(12,12))

#Draw
density_hood_price_plot = sns.violinplot(ax=ax, x='neighbourhood_group', y='price', hue='neighbourhood_group', data=data_price, palette='muted', dodge=False) 
density_hood_price_plot.set(xlabel="Neighbourhood Groups", ylabel="Price($USD)", title="Density of Neighbourhood Groups")

ylabels = ['${}'.format(x) for x in density_hood_price_plot.get_yticks()]
density_hood_price_plot.set_yticklabels(ylabels)
plt.show()


# ## Now we can have an actual look at where this is taking place geographically for a better visual understanding.

# In[15]:


#Using folium's heatmap to show most preferred areas

map = folium.Map([40.80, -73.80], zoom_start=11)
folium.plugins.HeatMap(data[['latitude','longitude']].dropna(), radius=8, gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(map)
display(map)


# In[16]:


##Looking at New york with clsuters to get a visual of where the data is coming from geographically 



Long = -73.80
Lat=40.80
locations = list(zip(data.latitude,data.longitude))

map1 = folium.Map(location=[Lat,Long], zoom_start=9)
FastMarkerCluster(data=locations).add_to(map1)
map1


# In[17]:


#Now putting the maps details into a scatter plot to get a better visualization


plt.figure(figsize=(12,8))
sns.scatterplot(x=data.longitude,y=data.latitude, hue=data.neighbourhood_group)
plt.show()

