import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
from django.core.files.images import ImageFile
import seaborn as sns


plt.switch_backend('Agg')

#WEB Funtion
def draw_from_dict(dicdata, RANGE, heng=0):
    by_value = sorted(dicdata.items(), key=lambda item: item[1], reverse=True)
    x = []
    y = []
    fig3 = io.BytesIO()

    plt.figure(figsize=(16, 8))
    for d in by_value:
        x.append(d[0])
        y.append(d[1])

    plt.grid()
    plt.ylabel('Total flight numbers', size=16)
    plt.xlabel('Arrival airport', size=16)
    plt.xticks(rotation=90)
    # plt.bar(x[0:RANGE], y[0:RANGE])
    sns.barplot(x=x[0:RANGE], y=y[0:RANGE], label='Number of Flights')
    plt.savefig('img/departure_arrival.png')
    plt.savefig(fig3, format="png")
    content_file3 = ImageFile(fig3)
    return content_file3

def airport_statistics(airport, start_date, end_date, graph_name):
    # Get airport data
    flight_weather = pd.read_csv('/Users/shuyewin/PycharmProjects/756finalProject/flightPricePredict/DataAnalyzing/flight_weather.csv').reset_index()
    flight_weather = flight_weather.drop('Unnamed: 0', axis=1)
    flight_weather = flight_weather.drop_duplicates()
    airport_data = flight_weather[flight_weather['departure_iata'] == airport]

    # Get data from assigned date
    start_index = airport_data[airport_data['flight_date'] == start_date].index.tolist()[0]
    end_index = airport_data[airport_data['flight_date'] == end_date].index.tolist()[0]
    airport_date = airport_data.loc[start_index: end_index, :]

    # Draw departure_arrival statics
    arrival_airport = airport_date['arrival_iata'].value_counts().to_dict()
    content_file3 = draw_from_dict(arrival_airport, len(arrival_airport))

    # Delay minutes
    delay_minutes = airport_date.groupby('flight_date').mean()['departure_delay']
    delay_data = airport_date['flight_date'].unique()
    fig = io.BytesIO()
    plt.title(graph_name)
    plt.figure(figsize=(15, 15))
    plt.xlabel('flight date')
    plt.ylabel('delay minutes')
    plt.xticks(rotation=45)
    plt.plot(delay_data, delay_minutes, linewidth=4, color='#EE7621', label='delay minutes')
    plt.legend()
    plt.grid()
    plt.savefig(fig, format="png")
    content_file = ImageFile(fig)



    df = airport_date['flight_status'].value_counts()
    y = df.values
    explode = []
    if len(df.keys()) == 5:
        explode = [0.2, 0, 0, 0, 0]
    else:
        explode = [0.2, 0, 0, 0, 0, 0]
    fig1 = io.BytesIO()
    plt.figure(figsize=(16, 8))
    plt.pie(y,
            labels=df.keys().to_list(),
            colors=["skyblue", "red", "green", "purple", "pink", "yellow"],
            shadow=True,
            explode=explode,
            autopct='%.2f%%',
            )
    plt.savefig(fig1, format="png")
    content_file1 = ImageFile(fig1)

    return content_file, content_file1, content_file3, graph_name
    # return airport_date