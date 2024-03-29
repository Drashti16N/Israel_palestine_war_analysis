# -*- coding: utf-8 -*-
"""israel_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iOYCStIucJd0Ufy9I-Lya3NTYIVeKr-J
"""

# Commented out IPython magic to ensure Python compatibility.
#Importing different Libraries:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px

# %matplotlib inline

#Read csv file(data):
df = pd.read_csv("/content/israel_palestine_war.csv")

#View few records of datasets:
df.head()

#Display total number of rows and columns in datasets:
print(df.shape)
print(f"total number of rows: {df.shape[0]}".upper())
print(f"total number of columns: {df.shape[1]}".upper())

#Display all the column name and their data types:
print(df.info())

#Check for null values in datasets:
print(df.isnull().sum())

#View the mean, std, min, max values of age:
print(df.describe())

"""
*   The average age of the dead is 26.
*   The youngest among the individuals dead was 1 yeal old baby.
*   The  oldest among the individuals dead was 112 year old."""

#Drop notes column from the dataframe:
df.drop("notes",inplace=True, axis=1)

#Check the number of columns decreased to 15 from 16:
df.shape

"""**# CLEANING DATASETS:**
* Dealing with NAN values:
"""

#Fill Nan values of age columns with mean value of age:
df['age'].fillna(df['age'].mean(), inplace=True)

#Fill Nan values of gender columns with mode of gender:
df['gender'].fillna(df['gender'].mode()[0], inplace=True)

df.dropna(subset=['took_part_in_the_hostilities'], inplace=True)

#Fill Nan values of place of residence and district columns with "unknow":
df['place_of_residence'].fillna('Unknown', inplace=True)
df['place_of_residence_district'].fillna('Unknown', inplace=True)

#Fill the Nan values of type of injury and ammunition columns with "Not specified":
df['type_of_injury'].fillna('Not Specified', inplace=True)
df['ammunition'].fillna('Not Specified', inplace=True)

#Check that all Nan values are filled or not:
print(df.isnull().sum())

#View number of rws and columns after data cleaning process:
df.shape

"""
*   **Converting date columns to pandas datetime:**"""

df['date_of_event'] = pd.to_datetime(df['date_of_event'])
df['date_of_death'] = pd.to_datetime(df['date_of_death'])

"""**# DATA VISULIZATION:**

* Age Distribution of Fatalities:
"""

# Ploting a histogram for the 'age' column:

#set figure size of graph:
plt.figure(figsize=(10, 6))

#create histogram and accordingly give parameters like colour, bins, edgecolour etc:
plt.hist(df['age'], bins=20, color='pink', edgecolor='purple')

#Give title of the graph:
plt.title('Distribution of Age'.upper())

#Give labels to x and y-axis:
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

"""*   The above graph represents the distribution by age of individuals killed in the war between israel and palestine.
*  From the graph we can say that majority of the peoples that are killed is of the age group 15 to 30. Young peoples are the biggest victims of the war.

*   Distribution of Fatalities by Citizenship:
"""

#Count and view the total number of peoples of israel and palestine in dataset:
citizenship_counts = df['citizenship'].value_counts()
print(f"citizenship counts:\n{citizenship_counts}".upper())

#plot the number of citizens of israel and palestine:
ax = sns.countplot(x='citizenship', data=df)

#set the partitions of y-axis for better visulization:
num_partitions = 15
ax.set_yticks(range(0, len(df) + 1, len(df) // num_partitions))

#Give title to the plot:
plt.title('Citizenship Distribution'.upper())
plt.show()

"""
*  Distribution of Fatalities by Gender:"""

#Replacing the M with "Male" and F with "Female" in gender column for better representation:
df['gender'].replace({'M': 'Male', 'F': 'Female'}, inplace=True)

#Count and view the male and females in dataset:
Gender_counts = df['gender'].value_counts()
print(f"Gender_counts:\n{Gender_counts}".upper())

#creating Pie Chart for Gender Distribution:
#set the figure size for graph:
plt.figure(figsize=(8, 5))

#create pie chart and accordinlgy set parameters like labels, startangle, colors, explode etc:
plt.pie(Gender_counts, labels=Gender_counts.index, autopct='%1.1f%%', startangle=140, colors=['y','r'], explode=[0,0.13])

#Give title to the chart:
plt.title('Gender Distribution'.upper())
plt.show()

"""
* Fatality Trends from 2000 to 2023:"""

# Group by date and count the number of fatalities:
fatalities_over_time = df.groupby('date_of_event').size()

# Create a time series plot:
#set figure size:
plt.figure(figsize=(12, 6))
fatalities_over_time.plot()

#Give title to the plot:
plt.title('Fatalities Over Time'.upper(), color= 'r')

#Give labels to x and y-axis:
plt.xlabel('Year',color= 'r')
plt.ylabel('Number of Fatalities',color= 'r')
plt.show()

"""
* Distribution of Place of Residence:"""

# Categorical Analysis - Place of Residence (Top N)
a = 10  # Set the number of top categories to display

# Get the top N categories:
a_categories = df['place_of_residence'].value_counts().nlargest(a).index

# Replace less frequent categories with 'Other':
df['place_of_residence_top_n'] = df['place_of_residence'].apply(lambda x: x if x in a_categories else 'Other')

#set figure size:
plt.figure(figsize=(12, 6))
b = sns.countplot(x='place_of_residence_top_n', data=df)

#Give title to the plot:
plt.title('Distribution of Place of Residence (Top {})'.format(a).upper())

#set rotation of the x lables:
plt.xticks(rotation=30)
plt.show()

"""
* Distribution of Types of Injuries:"""

# Count the occurrences of each type of injury:
injury = df['type_of_injury'].value_counts()
print(injury)

#plot the line graph of type of injury:
#set figure size:
plt.figure(figsize=(10, 6))

#plot graph and set color to red:
injury.plot( color='red')

#Give title to the plot:
plt.title('Distribution of Types of Injuries'.upper())

#Give labels to x and y-axis:
plt.xlabel('Type of Injury')
plt.ylabel('Count')
plt.show()

"""* The graph shows the distribution of death with different instruments.
* The graph shows that 91 per cent of deaths were by gunfire.

* Distribution Based on Participation in Hostilities:
"""

# Count the number of occurrences for each category in 'took_part_in_the_hostilities':
participation_counts = df['took_part_in_the_hostilities'].value_counts()
participation_counts

# Create a bar plot to visualize the extent of participation:
#set figure size:
plt.figure(figsize=(10, 6))
plt.bar(participation_counts.index, participation_counts.values, color='skyblue')

for i, count in enumerate(participation_counts.values):
    plt.text(i, count + 5, str(count), ha='center', va='bottom')

#give title to plot:
plt.title('Extent of Participation in Hostilities'.upper())

#give labels to x and y-axis:
plt.xlabel('Participation Status')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

#Create Pie Chart to visualize the extent of participation:
plt.figure(figsize=(8, 5))
plt.pie(participation_counts, labels=participation_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'),labeldistance=1.13, wedgeprops = { 'linewidth' : 0.5, 'edgecolor' : 'black' })
plt.title('Extent of Participation in Hostilities'.upper(),color='r')
plt.show()

"""*  The graph shows that the majority of the dead had no participation in
the hostilities, accounting for 48 per cent of the total dead.
*  Next, we can see that 36 per cent of the dead took part in the hostilities.

* Also 6 per cent are not known, 8 per cent were killed by the Israelis, while 2 per cent of the dead were targeted.

* Type of ammunition and means of killing:
"""

# Count and view the occurrences of each type of ammunition and means of killing:
ammunition_counts = df['ammunition'].value_counts()
means_of_killing_counts = df['killed_by'].value_counts()

print(f"Ammunition used:\n{ammunition_counts}".upper())

print(f"\nMeans of killing:\n{means_of_killing_counts}".upper())

#create two bar plots of most used ammunition and means of killing:
#set figure size:
plt.figure(figsize=(12, 6))

# Plot ammunition:
plt.subplot(1, 2, 1)
ammunition_counts.head(10).plot(kind='bar', color='orange')

#Give title to plot:
plt.title('Top 10 Most Used Ammunition'.upper(),color= 'r')

#Give labels to x and y-axis:
plt.xlabel('Ammunition',color= 'r')
plt.xticks(rotation=25)
plt.ylabel('Count',color= 'r')

# Plot means of killing:
plt.subplot(1, 2, 2)
means_of_killing_counts.head(10).plot(kind='bar', color='green')

#Give title to plot:
plt.title('Top 10 Means of Killing'.upper(),color= 'r')

#Give labels to x and y-axis:
plt.xlabel('Means of Killing',color= 'r')
plt.xticks(rotation=25)
plt.ylabel('Count',color= 'r')

plt.tight_layout()
plt.show()

"""* The above graph shows the distributions of aummunition and means of killing.

* Distribution of Fatalities by District:
"""

df['year'] = df['date_of_event'].dt.year

# Choose the top N places to focus on:
top_n_places = 15

# Get the top N places with the highest total fatalities:
top_places = df['place_of_residence'].value_counts().nlargest(top_n_places).index

# Filter the data to include only the top N places:
filtered_data = df[df['place_of_residence'].isin(top_places)]

# Group by place and year, and sum the number of fatalities:
fatalities_by_place = filtered_data.groupby(['place_of_residence', 'year']).size().reset_index(name='fatalities_count')

# Create a line plot for each place:
plt.figure(figsize=(12, 8))
for place in top_places:
    data = fatalities_by_place[fatalities_by_place['place_of_residence'] == place]
    plt.plot(data['year'], data['fatalities_count'], label=place)

#Give title and labels to the axis of the plot:
plt.title(f'Fatality Trends for Top {top_n_places} Places'.upper(),color= 'r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Number of Fatalities',color= 'r')
plt.legend()
plt.show()

"""* The above graph shows the trend of number of deaths over the years of different districts(area).

* Representation of major districts on map:
"""

#Defining the approximate coordinates for major districts:
district_coords = {
    'Gaza': [31.5, 34.466667],
    'Hebron': [31.532569, 35.095388],
    'Jenin': [32.457336, 35.286865],
    'Nablus': [32.221481, 35.254417],
    'Ramallah': [31.902922, 35.206209],
    'Bethlehem': [31.705791, 35.200657],
    'Tulkarm': [32.308628, 35.028537],
    'Jericho': [31.857163, 35.444362],
    'Rafah': [31.296866, 34.245536],
    'Khan Yunis': [31.346201, 34.306286],
    'Tubas':[32.3211, 35.3700],
    'North Gaza':[31.5417, 34.5196],
    'Ramallah and al-Bira':[31.9486, 35.1709],
    'al-Quds':[31.7683, 35.2137],
    'Deir al-Balah':[31.4171, 34.3509]
}
# Get fatality counts for each district:
district_fatalities = df.groupby('event_location_district').size()

# Function to determine the color of the circle based on the number of fatalities:
def get_color(fatalities):
    if fatalities > 500:
        return 'darkred'
    elif fatalities > 100:
        return 'red'
    elif fatalities > 50:
        return 'orange'
    else:
        return 'green'

# Create a base map centered around the region:
m = folium.Map(location=[31.5, 34.75], zoom_start=8, tiles='OpenStreetMap')

# Add markers and circles for districts:
for district, coords in district_coords.items():
    fatalities = district_fatalities.get(district, 0)
    folium.Marker(
        location=coords,
        tooltip=f'{district}: {fatalities} fatalities',
        icon=None
    ).add_to(m)
    folium.Circle(
        location=coords,
        radius=np.sqrt(fatalities) * 1000,  # scale radius for better visualization
        color=get_color(fatalities),
        fill=True,
        fill_color=get_color(fatalities),
        fill_opacity=0.6,
    ).add_to(m)

# Add layer control:
folium.LayerControl().add_to(m)
m

"""Palestine:"""

#Extract palestian data:
palestinian_data = df[df['citizenship'] == 'Palestinian']
a = palestinian_data['date_of_event'].tolist()

palestinian_data

#Make list of only year from entire date:
b = []
for i in a:
  b.append(str(i)[0:4])
print(b)

palestinian_data['Year'] = b

#make one list of year and another list of count of death in palestine:
list_1= []
list_2= []
for i in range(2000,2024):
  list_1.append(i)
  list_2.append(b.count(str(i)))
print(list_1)
print(list_2)

#Make dataframe of year and count of death in palestine:
Df_new = pd.DataFrame({'Year':list_1,'count':list_2})
print(Df_new)

# creating the bar plot of deaths in palestine:
plt.barh(Df_new['Year'], Df_new['count'], color ='maroon')

#Give title and labels to x and y-axis:
plt.xlabel("Number of Fatalities".upper())
plt.ylabel("Year")
plt.title("Palestinian Fatalities (2000-2023)")
plt.show()

"""* 1. The above graph shows the total number of deaths over years in palestine.

Israel
"""

#Extract israel data:
israel_data = df[df['citizenship'] == 'Israeli']
c = israel_data['date_of_event'].tolist()

#Make list of only year from entire date:
d = []
for j in c:
  d.append(str(j)[0:4])
print(d)

israel_data['Year'] = d

#make one list of year and another list of count of death in israel:
list_3= []
list_4= []
for j in range(2000,2024):
  list_3.append(j)
  list_4.append(d.count(str(j)))
print(list_3)
print(list_4)

#Make dataframe of year and count of death in israel:
Df_i = pd.DataFrame({'Year':list_3,'count':list_4})
print(Df_i)

# creating the bar plot of death in israel:
plt.barh(Df_i['Year'], Df_i['count'], color ='green')

#Give title and labels to x and y-axis of the plot:
plt.xlabel("Number of Fatalities".upper())
plt.ylabel("Year")
plt.title("Palestinian Fatalities (2000-2023)")
plt.show()

"""* 1. The above graph shows the total number of deaths over years in israel.

# **Use of 2nd dataset for GDP analysis of isreal and palestine:**
"""

#Read and view csv file of dataset:
df_1 = pd.read_csv("/content/Israel-Palestine_gdp.csv")
df_1.head()

#Display total number of rows and columns in datasets:
print(df_1.shape)
print(f"total number of rows: {df_1.shape[0]}".upper())
print(f"total number of columns: {df_1.shape[1]}".upper())

#Display all the column name and their data types:
df_1.info()

"""
* changing data types:"""

#Changing datatypes to float:
def obj_to_float(i):
    if 'million' in i.lower():
        return float(i.replace('million',''))*1e6
    elif 'billion' in i.lower():
        return float(i.replace('billion',''))*1e9
    else: None


df_1['GDP (in USD)'] = df_1['GDP (in USD)'].apply(lambda x:obj_to_float(str(x)))
df_1['Agricultural Output (in USD)'] = df_1['Agricultural Output (in USD)'].apply(lambda x:obj_to_float(str(x)))
df_1['IT Output (in USD)'] = df_1['IT Output (in USD)'].apply(lambda x:obj_to_float(str(x)))

df_1.head()

cols = ['Population', 'Active Military Personnel', 'Reserve Military Personnel','Number of Tanks','Number of Armoured Vehicles']
for i in cols:
    df_1[i]=df_1[i].str.replace(",",'').astype(float)

df_1.head()

#Check changed data types:
df_1.info()

"""# **Data Visualization:**

*  Comparison between the two countries:

* GDP Over the Years (USD):
"""

#Comparision line chart of GDP over years of israel and palestine:
fig = px.line(df_1, x='Year', y='GDP (in USD)', color='Country', markers=True, title= 'GDP Over the Years (USD)')
fig.show()

"""*  The above graph shows the GDP in USD of israel and palestine over year.

* Population Growth Over the Years:
"""

# Create a bar plot to visualize Population Growth Over the Years:
plt.figure(figsize=(10, 6))
plt.bar(df_1['Year'], df_1['Population'], color='orange')

#Give title and labels to the axises:
plt.title('Population Growth Over the Years'.upper(),color= 'r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Population',color= 'r')
plt.xticks(rotation=45)
plt.show()

"""GDP Growth (%) Over the Years"""

#Plot #Comparision line chart of GDP in % over years of israel and palestine:
fig = px.line(df_1, x='Year', y='GDP Growth Rate (%)', color='Country', markers=True, title = 'GDP Growth (%) Over the Years')
fig.show()

#Extracting israel data:
israel_df = df_1[df_1['Country']=="Israel"]
israel_gdp= israel_df['GDP Growth Rate (%)']

#Extracting plasestine data:
palestine_df= df_1[df_1['Country']=="Palestine"]
palestine_gdp= palestine_df['GDP Growth Rate (%)']

#Plot Fertility rate over years:
#Set figure size:
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)

#Plot line chart and accordingly set parameter like color:
plt.plot(israel_df['Year'],israel_df['Fertility Rate'],color='black')

#Give title and labels to axis:
plt.title('Fertility Rate of israel over years'.upper(),color= 'r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Fertility Rate',color= 'r')

plt.subplot(1, 2, 2)

#Plot line chart and accordingly set parameter like color:
plt.plot(palestine_df['Year'],palestine_df['Fertility Rate'],color='blue')

#Give title and labels to axis:
plt.title('Fertility Rate of palestine over years'.upper(),color= 'r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Fertility Rate',color= 'r')

plt.tight_layout()
plt.show()

"""
* The above figure have two line charts of fertility rate over the years. 1st represents it for israel and 2nd for palestine.
"""

#Plot Agricultural output over years:
#Set figure size:
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)

#Plot line chart and accordingly set parameter like color:
plt.plot(israel_df['Year'],israel_df['Agricultural Output (in USD)'],color='maroon')

#Give title and labels to axis:
plt.title('Agricultural Output (in USD) of israel over years'.upper(),color='r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Agricultural Output (in USD)',color='r')

plt.subplot(1, 2, 2)

#Plot line chart and accordingly set parameter like color:
plt.plot(palestine_df['Year'],palestine_df['Agricultural Output (in USD)'],color='darkgreen')

#Give title and labels to axis:
plt.title('Agricultural Output (in USD) of palestine over years'.upper(),color= 'r')
plt.xlabel('Year',color= 'r')
plt.ylabel('Agricultural Output (in USD)',color= 'r')

plt.tight_layout()
plt.show()

"""
* The above figure have two line charts of Agricultural output over the years. 1st represents it for israel and 2nd for palestine.
* In both israel and palestine it is decreasing from 2020-2021.
"""