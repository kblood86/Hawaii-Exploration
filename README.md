# Hawaii Exploration

![surfs-up.png](Images/surfs-up.png)

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area.

## Let's look at the climate!

-This exploration was done using the provided starter notebook and the Hawaii dataset

-SQLAlchemy was used to connected to our dataset then to reflect the tables into classes and save a reference. These references were called 'Station' and Measurement"

-Python was linked to the database by creating a SQLAlchemy session

-To start the analysis we found the most recent date in the data

-Working backwards, we found the date a year prior to this query and pulled the year's worth of precipitation data.

-A data frame using only the date and precipitation values was created and the index was set to the date column.

-This data was used to create a bar chart seen below:

![precip](https://user-images.githubusercontent.com/77282780/120549474-a6d4cb00-c3c1-11eb-9ee5-045646a72da2.png)

-Pandas was used to print summary statistics for this data


* **Important** Don't forget to close out your session at the end of your notebook.


### Station Analysis

-We created a query to calculate the total number of stations in the dataset.

-From here we found the most active station and listed them and the number of observations at each in descending order.

-For the most active station in the data, we found the maximum, mimimum, and average temperature.

-A query was designed to pull the last 12 months of temperatures observed (TOBS) and a histogram was created:

![TOBS](https://user-images.githubusercontent.com/77282780/120550277-a557d280-c3c2-11eb-8db7-7d95443c4950.png)


-The session was closed.

- - -

## Creating a climate app

-Next a Flask API was designed a Flask API based on the queries. All data is returned as a json list

-From the home page you can navigate to:

  * `/api/v1.0/precipitation`: Precipitation data from the last year

  * `/api/v1.0/stations`: List of stations from the dataset.
 
  * `/api/v1.0/tobs`: Dates and temperature observations of the most active station for the last year of data

  * `/api/v1.0/<start>`: List of the minimum temperature, the average temperature, and the max temperature for a given start date
  
  * `/api/v1.0/<start>/<end>`: List of the minimum temperature, the average temperature, and the max temperature for a given date range


