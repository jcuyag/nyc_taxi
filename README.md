------------
This code utilizes `panda` for the data frame and `matplotlib` to visualize the dataset. It supports Python 3.6

Installation
------------
Clone this project and install the requirements.txt via pip command.
    
    pip install -r requirements.txt

Usage
-----
Place the taxi rides CSV file on the data folder. The source code doesn't merge all data content due to the large amount of data. Instead the code read one CSV file at a time by manually changing line numer 5 to the desired CSV file.

Run the python code
 
    python ny_taxi.py

This will print the data set and generate image files for plotting the data to diagram.

The file `daily_manhattan_to_JFK_trip.png` is filtered number of trips from Manhattan to JFK Airport on a daily basis.
The file `daily_precipitation.png` is the precipitation information from the daily number of trips.
