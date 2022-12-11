import pandas as pd
import time
import os
import json
import urllib.request
import urllib
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings


def get_weather_data():
    '''
    get weather data from api, preprocess and save in csv file
    :return:
    '''
    print("getting weather data")

    with urllib.request.urlopen('https://danepubliczne.imgw.pl/api/data/synop/station/jeleniagora') as url:
        record = json.load(url)

    df = pd.json_normalize(record)
    df.drop(['id_stacji', 'stacja'], inplace=True, axis=1)
    if os.path.exists(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_weather.csv')):
        df.to_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_weather.csv'), mode='a', index=False, header=False)
    else:
        df.to_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_weather.csv'), mode='a', index=False, header=True)


def get_smog_data():
    '''
    get smog data from api, select record from Warchałowskiego 8, preprocess and save in csv file
    :return:
    '''
    print("getting smog data")
    with urllib.request.urlopen(
            "https://api.um.warszawa.pl/api/action/air_sensors_get/?apikey=57032d82-2e4c-4b75-a2ca-26a37dee9833") as url:
        record = json.load(url)

    if record != {'result': 'Błędna metoda lub parametry wywołania'}:
        df = pd.DataFrame(record['result'])
        df = df[
            df['station'] == 'Warchałowskiego 8']  # select records from one localization - Warchałowskiego 8 (Ursynów)
        df = df[['ijp', 'data']]
        tmp_cols = ['PM10_tmp', 'PM2.5_tmp', 'PM1_tmp', 'NO2_tmp']
        df[tmp_cols] = pd.DataFrame(df['data'].to_list(), index=df.index)
        df.drop('data', inplace=True, axis=1)
        df['PM10'] = df.apply(lambda x: x['PM10_tmp']['value'], axis=1)
        df['PM2.5'] = df.apply(lambda x: x['PM2.5_tmp']['value'], axis=1)
        df['PM1'] = df.apply(lambda x: x['PM1_tmp']['value'], axis=1)
        df['NO2'] = df.apply(lambda x: x['NO2_tmp']['value'], axis=1)
        # split date & time into 2 columns
        df['date'] = df.apply(lambda x: x['PM10_tmp']['time'].split(' ')[0], axis=1)
        df['time'] = df.apply(lambda x: x['PM10_tmp']['time'].split(' ')[1], axis=1)
        df.drop(tmp_cols, axis=1, inplace=True)
        df.drop('ijp', axis=1, inplace=True)
        if os.path.exists(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_smog.csv')):
            df.to_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_smog.csv'), mode='a', index=False, header=False)
        else:
            df.to_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_smog.csv'), mode='a', index=False, header=True)


def run():
    '''
    every 10 minutes download smog data &
    every 1 hour download weather data
    :return:
    '''
    scheduler = BackgroundScheduler()
    # save smog data form API every 10 minutes:
    scheduler.add_job(get_smog_data, 'interval', minutes=10)
    # save weather data form API every hour:
    scheduler.add_job(get_weather_data, 'interval', minutes=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


def merge_smog_weather():
    '''
    merge dataframes with smog and weather data
    :return:
    '''
    smog_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_smog.csv'))
    weather_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_weather.csv'))

    weather_df.rename(columns={'data_pomiaru': 'date', 'godzina_pomiaru': 'time'}, inplace=True)
    # add temporary column for joining - e.g. 17 instead of 17:10:00
    smog_df['time_tmp'] = pd.to_datetime(smog_df["time"], format='%H:%M:%S').dt.hour
    weather_df['time_tmp'] = weather_df['time'].astype(str).astype(int)
    weather_df.drop('time', inplace=True, axis=1)

    # join tables
    df = pd.merge(smog_df, weather_df, how='inner', left_on=['date', 'time_tmp'], right_on=['date', 'time_tmp'])
    df.drop("time_tmp", axis=1, inplace=True)
    df.to_csv(os.path.join(settings.BASE_DIR, 'backend', 'model', 'data_merged.csv'), index=False)
