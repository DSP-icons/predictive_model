import pandas as pd

def filter_time_series_according_to_pairs(time_series, pairs):
    ''' This function filters the time series according to the pairs of country and disaster type'''
    return time_series[ time_series.apply(lambda row: (row["Country"], row["Disaster Type"]) in pairs, axis=1) ]


df1 = pd.read_csv('DISASTERS/1900_2021_DISASTERS.xlsx - emdat data.csv')
df2 = pd.read_csv('DISASTERS/1970-2021_DISASTERS.xlsx - emdat data.csv')
df = pd.concat([df1, df2], axis=0)

# Exclude biological and extra-terrestrial disasters
df = df[~df["Disaster Subgroup"].isin(["Biological", "Extra-Terrestrial"])]

# Select the columns of interest
df = df[['Year', 'Country', 'Disaster Type']]

# Filter the data to only include the top 3 countries
top_countries = df["Country"].value_counts()[:3]
df = df.query('Country in @top_countries.index')

# Count amount of disasters by year, country and disaster type
time_series = df.groupby(['Year', 'Disaster Type', 'Country']).size().reset_index(name='Count')

# Transpose the data to have the years as columns, making each row as a time series
time_series = time_series.pivot_table(index=["Country", "Disaster Type"], columns="Year", values="Count").reset_index()
time_series = time_series.fillna(0)

# Filter the time series according to the pairs of country and disaster type
disaster_types_by_country = {
    "United States of America (the)" : ["Storm", "Flood", "Wildfire"],
    "China" : ["Flood", "Storm", "Earthquake"],
    "India" : ["Flood", "Storm", "Extreme temperature "]
}
pairs = [ (country, disaster_type) for country in disaster_types_by_country.keys() for disaster_type in disaster_types_by_country[country] ]

# Get the data of countries and disaster types of interest
time_series = filter_time_series_according_to_pairs(time_series, pairs)

# Take the data from 2000 onwards
year_2000_index = time_series.columns.get_loc(1980)
time_series = time_series.iloc[:, [0, 1] + list(range(year_2000_index, time_series.shape[1]))]

time_series.to_csv("time_series.csv", index=False)