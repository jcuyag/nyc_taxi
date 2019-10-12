import matplotlib.pyplot as plt
import pandas as pd

# concat other CSV file soon
DF = pd.read_csv('data//yellow_tripdata_2017-12.csv')

LOC = pd.read_csv('taxi+_zone_lookup.csv')

WTR = pd.read_csv('NOAA_Central_Park_data.csv')

JFK_ID = 132

class NYTaxi:
    def __init__(self):
        self.tx_df = DF
        self.loc_df = LOC
        self.man_list = self._get_manhattan_ids()
        self.wx = WTR

    def _get_manhattan_ids(self):
        _man = self.loc_df[(self.loc_df.Borough == 'Manhattan')]
        return _man.LocationID.to_list()
        
    def filter_time_location(self):
        return self.tx_df.filter(['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID'])

    def filter_man_to_jfk(self):
        df = self.filter_time_location()
        _pu_filter = (df.PULocationID.isin(self.man_list))
        _do_filter = (df.DOLocationID == JFK_ID)
        return df[_pu_filter & _do_filter]

    def daily_man_to_jfk(self):
        df = self.filter_man_to_jfk()
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df.index = df['tpep_pickup_datetime']
        fdf = df.filter(['PULocationID', 'DOLocationID'])
        
        return fdf.index.day.value_counts().sort_index()

    def merge_daily_trip_weather(self):
        df_tr = self.filter_man_to_jfk()
        df_wx = self.wx.filter(['DATE', 'PRCP'])

        # convert date and set to index
        df_tr.tpep_pickup_datetime = pd.to_datetime(df_tr.tpep_pickup_datetime)
        df_tr.index = df_tr.tpep_pickup_datetime

        
        df_wx.DATE = pd.to_datetime(df_wx.DATE)
        df_wx.index = df_wx.DATE

        daily_trp = df_tr.resample('B').mean()
        
        _merged = pd.merge(daily_trp, df_wx, left_index=True, right_index=True)
        
        return _merged.filter(['DATE', 'PRCP'])

    def plot_trip(self, df):
        df.plot(kind='bar',x='index',y='tpep_pickup_datetime')
        plt.savefig('daily_manhattan_to_JFK_trip.png')
    
    def plot_weather(self, df):
        df.plot(kind='line',x='DATE',y='PRCP', color='red')
        plt.savefig('daily_precipitation.png')


if __name__ == "__main__":

    nyt = NYTaxi()

    trip = nyt.filter_man_to_jfk()
    daily_trip = nyt.daily_man_to_jfk()
    print(trip)

    wx = nyt.merge_daily_trip_weather()
    print(wx)

    nyt.plot_trip(daily_trip)
    nyt.plot_weather(wx)