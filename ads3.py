# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:56:58 2023

@author: shan
"""


# Function to read the name of the dataset and return two datasets
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis


def read_data(data):
    # Reading the data
    try:
        df = pd.read_csv(
            r'C:\Users\shanf\OneDrive\Desktop\ads3\%s' %
            data, on_bad_lines='skip')
    except pd.errors.ParserError:
        print(f"Error parsing file {data}")
        return None

    # Transpose the data and name the new column as 'Years'
    t_df = df.transpose().reset_index()
    t_df.columns = t_df.iloc[0]
    t_df = t_df[1:]

    return df, t_df


df, t_df = read_data('climate_change.csv')  # Getting the two datasets
df.head()

# Checking all the available indicators
df['Indicator Name'].unique()

# Transposed DataFrame
t_df.head()

# Creating 3 dataframes with 3 indicators by subsetting the original dataframe
df_accelec = df[df['Indicator Name'] ==
                'Access to electricity (% of population)']
df_pop = df[df['Indicator Name'] ==
            'Population growth (annual %)']
df_co2 = df[df['Indicator Name'] ==
            'CO2 emissions from solid fuel consumption (% of total)']


# Merging the 3 dataframes
df_merge = pd.concat([df_accelec, df_pop, df_co2])
df_merge.head()

# Resetting the index
df_merge.reset_index(inplace=True, drop=True)

# replace '..' values with NaN values in data
df_merge.replace('..', np.nan, inplace=True)
# removing the past 4 years since there is very little data
df_merge = df_merge.iloc[:, :-3]

# replacing missing values with 0
df_merge.fillna('0', inplace=True)  # replacing NaN with 0's
# dropping redundant columns
df_merge.drop(['Indicator Code', 'Country Code'], axis=1, inplace=True)

years = df_merge.columns[2:]
# removing wrong values final time
df_merge.replace('..', 0, inplace=True)

# Converting the data to numeric and rounding off to 2 decimals
df_merge[years] = np.abs(df_merge[years].astype('float').round(decimals=2))


# Grouping by 'Indicator Name' column and plotting the size of each group
df_merge.groupby(['Indicator Name'])['1960'].size().plot(kind='bar')
plt.title('Size of each group')
plt.xticks(rotation=90, ha='center')
plt.tick_params(axis='x', width=1, pad=10, length=0)
plt.show()


# Subset the data by selecting countries, indicators, and years of
# interest for CO2 emissions
countries = [
    'Niger',
    'Afghanistan',
    'Japan',
    'Germany',
    'United Kingdom',
    'France',
    'Italy',
    'United States',
    'Mexico',
    'Belgium',
    'India',
    'Finland']
indicator = 'CO2 emissions from solid fuel consumption (% of total)'
years = [
    '2010',
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016',
    '2017',
    '2018']

data = df_merge.loc[df_merge["Country Name"].isin(countries) & df_merge["Indicator Name"].eq(
    indicator), ["Country Name", "Indicator Name"] + years]
# Create the grouped bar chart
ax = data.plot(kind="bar", x="Country Name", figsize=(10, 6))
ax.set_xlabel("Country")
ax.set_ylabel("CO2 emissions from solid fuel consumption")
ax.set_title("CO2 emissions by Country (2009-2015)")
plt.legend(title="Year", loc="upper right")
plt.savefig('change.jpeg')
plt.show()

# Subset the data by selecting countries, indicators, and years of
# interest for population growth
countries = [
    'Niger',
    'Afghanistan',
    'Japan',
    'Germany',
    'United Kingdom',
    'France',
    'Italy',
    'United States',
    'Mexico',
    'Belgium',
    'India',
    'Finland']
indicator = 'Population growth (annual %)'
years = [
    '2010',
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016',
    '2017',
    '2018']

data = df_merge.loc[df_merge["Country Name"].isin(countries) & df_merge["Indicator Name"].eq(
    indicator), ["Country Name", "Indicator Name"] + years]
# Create the grouped bar chart
ax = data.plot(kind="bar", x="Country Name", figsize=(10, 6))
ax.set_xlabel("Country")
ax.set_ylabel("Population growth (annual %)")
ax.set_title("Population growth by Country (2009-2015)")
plt.legend(title="Year", loc="best")
plt.savefig('change.jpeg')
plt.show()

# Using describe() to get the summary statistics of the merged dataframe
print(df_merge.loc[:, '2000':'2018'].describe())

# Select only numeric columns
numeric_cols = df_merge.select_dtypes(include=np.number).columns.tolist()

# Compute skewness and kurtosis for each numeric column
for col in numeric_cols:
    skewness = skew(df_merge[col])
    kurt = kurtosis(df_merge[col])
    print(f"Column {col}: Skewness = {skewness:.2f}, Kurtosis = {kurt:.2f}")

# diving the data back to 3 datasets to perform summary statistics
df_merge_accelec = df_merge[df_merge['Indicator Name']
                            == 'Access to electricity (% of population)']
df_merge_pop = df_merge[df_merge['Indicator Name'] ==
                        'Population growth (annual %)']
df_merge_co2 = df_merge[df_merge['Indicator Name'] ==
                        'CO2 emissions from solid fuel consumption (% of total)']


# saving the summary statistics in a dataframe
stats = pd.DataFrame()
stats['accelec'] = df_merge_accelec[years].mean(axis=0).to_frame()
stats['pop'] = df_merge_pop[years].mean(axis=0).to_frame()
stats['co2'] = df_merge_co2[years].mean(axis=0).to_frame()

# select columns for the years 2000 to 2018
stats = stats.loc['2010':'2018']

# scaling the data since all the groups are not in the same scale
scaler = StandardScaler()

# scaling the data using standard scaler and saving it with full column names
stats_sc = pd.DataFrame(
    scaler.fit_transform(stats),
    columns=[
        'Access to electricity (% of population)',
        'Population growth (annual %)',
        'CO2 emissions from solid fuel consumption (% of total)'])

stats_sc.index = stats.index  # set the index to be the same as the stats DataFrame

# plotting the general trend of the 3 groups over the years
plt.figure(figsize=(6, 6))  # size of the image
for i in stats_sc.columns:
    plt.plot(stats_sc.index, stats_sc[i], label=i)  # plotting the 3 lines
plt.legend(loc='best')  # setting the location of the legends
plt.xticks(stats_sc.index, rotation=45)  # changing the x axis values
plt.xlim('2010', '2018')  # set the limits for the x axis
plt.ylabel('Relative Change')  # setting y axis label
plt.title('Change of Indicators over the years all over the world')
plt.savefig('trend.jpeg')  # saving the image
plt.show()

usa = df_merge[df_merge['Country Name'] == 'Afghanistan']
usa = usa.drop(['Country Name'], axis=1)
usa = usa.set_index('Indicator Name').T

ind = df_merge[df_merge['Country Name'] == 'Belgium']
ind = ind.drop(['Country Name'], axis=1)
ind = ind.set_index('Indicator Name').T


def plot_country(data, name):
    plt.figure(figsize=(6, 6))
    for i in data.columns:
        # Select only the data for the years 2000 to 2018
        data_range = data.loc['2010':'2018', [i]]

        scaler = StandardScaler()
        # scaling the data using standard scaler and saving it with full column
        # names
        country_sc = pd.DataFrame(
            scaler.fit_transform(data_range), columns=[i])
        country_sc.index = data_range.index
        plt.plot(
            country_sc.index,
            country_sc[i],
            label=i)  # plotting the line
        plt.legend(loc='best')  # setting the location of the legends
        plt.xticks(country_sc.index, rotation=45)  # changing the x axis values
        plt.ylabel('Relative Change')  # setting y axis label
    plt.title(
        'Change of Indicators over the years in %s' %
        name)  # setting the title
    plt.show()


plot_country(usa.loc['2010':'2018'], 'Afghanistan')
plot_country(ind.loc['2010':'2018'], 'Belgium')


corr_mat = stats_sc.corr()  # calculating the correlation of the data
fig, ax = plt.subplots(figsize=(10, 10))  # size of the figure
im = ax.imshow(corr_mat, cmap='coolwarm')  # plotting the heatmap

# adding the values inside each cell
for i in range(len(corr_mat)):
    for j in range(len(corr_mat)):
        text = ax.text(j, i, round(
            corr_mat.iloc[i, j], 2), ha="center", va="center", color="black")

# setting the labels
ax.set_xticks(np.arange(len(corr_mat.columns)))
ax.set_yticks(np.arange(len(corr_mat.columns)))
ax.set_xticklabels(corr_mat.columns)
ax.set_yticklabels(corr_mat.columns)

# rotating the x axis labels
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")

# adding the color bar
cbar = ax.figure.colorbar(im, ax=ax)

# setting the title
ax.set_title("Correlation Heatmap")

# saving and showing the image
plt.savefig('correlation_heatmap.png')
plt.show()
