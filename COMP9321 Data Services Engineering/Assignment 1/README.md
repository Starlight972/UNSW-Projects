# Question 1

Perform the following preprocessing steps:
- Drop all rows from the "exposure" dataset without country name
- Join the two datasets (exposure.csv and Countires.csv) based on the "country" columns in the datasets, keeping the rows as long as there is a match between the country columns of both dataset (do not concatenate the datasets)
You must ensure the countries with name issues match (e.g., USA and United States) but ignore if a country does not exist in either of datasets (e.g., Sudan and "South Sudan" are not the same)
- Keep only a single country column
- Set the index of the resultant dataframe as 'Country'
- Sort the dataset by the index (ascending)

# Question 2: ( based on the dataframe created in Question-1 )

The "Cities" column is a complex string, containing information about cities (e.g., latitude and longitude) of the corresponding country; you should **explore** the content of this column for each country and ***add two new columns*** to the dataframe called: **avg_latitude** and ****avg_longitude** ."avg_latitude" is the average latitude for all cities of the corresponding country, and "avg_longitude" is the average longitude for all cities of the same country.
