import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import copy
import pickle
import warnings

warnings.filterwarnings(action='ignore')


def date_to_int(df):
    df['hour'] = pd.to_datetime(df["time"], format='%H:%M:%S').dt.hour
    df['date'] = pd.to_datetime(df["date"], format='%Y-%m-%d')
    df['year'] = df["date"].dt.year
    df['month'] = df["date"].dt.month
    df['day'] = df["date"].dt.day
    df = df.drop('time', axis=1)
    return df


def count_avg_of_all_col(df: pd.DataFrame) -> pd.DataFrame:
    grouped_mean = df.groupby(['year', 'month', 'day', 'hour']).mean()
    df = df.merge(grouped_mean, how='left', on=['year', 'month', 'day', 'hour'], suffixes=['', '_avg'])
    return df


def add_lagged_variables(df: pd.DataFrame, cols: list, start: int, end: int) -> pd.DataFrame:
    for col in cols:
        for i in range(start, end):
            df[f'{col}_lag{i}'] = df[f'{col}'].shift(i)
    return df


def preprocessing(path: str) -> pd.DataFrame:
    raw_data = pd.read_csv(path)
    raw_data = raw_data.drop(columns=['recommendations', 'level'])
    raw_data = raw_data.sort_values(by=['date', 'time'], ascending=[True, True])
    raw_data = date_to_int(raw_data)
    raw_data = count_avg_of_all_col(raw_data)
    raw_data = raw_data.drop_duplicates(subset=['hour', 'day', 'month', 'year'])
    raw_data = raw_data.drop(
        ['PM10', 'PM2.5', 'PM1', 'NO2', 'temperatura', 'predkosc_wiatru', 'wilgotnosc_wzgledna', 'suma_opadu',
         'cisnienie', 'kierunek_wiatru'], axis=1)
    raw_data = raw_data.drop_duplicates()
    return raw_data


def split_data(df: pd.DataFrame):
    df = df.drop(columns='date')
    df_train = copy.deepcopy(df[df['day'] != 2])
    df_test = copy.deepcopy(df[df['day'] == 2])
    df_train = add_lagged_variables(df_train, ['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg'], 1, 5)
    df_train = df_train.dropna()
    y_test = df_test[['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg']]
    X_test = df_test.drop(columns=['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg'])
    y_train = df_train[['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg']]
    X_train = df_train.drop(columns=['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg'])
    return X_train, X_test, y_train, y_test, df_train, df_test


def create_model(X, y):
    rf = MultiOutputRegressor(RandomForestRegressor(n_estimators=10, random_state=43))
    rf.fit(X, y)
    return rf


def adjust_lagged_vars_for_y_test(rf: MultiOutputRegressor, df_train: pd.DataFrame, X_test: pd.DataFrame) -> list:
    predicted = []
    i = -1
    for row in X_test.to_dict(orient='records'):
        if i == -1:
            for j in range(1, 5):
                row.update({f'PM10_lag{j}': df_train['PM10_avg'].iloc[-j]})
                row.update({f'PM2.5_lag{j}': df_train['PM2.5_avg'].iloc[-j]})
                row.update({f'PM1_lag{j}': df_train['PM1_avg'].iloc[-j]})
                row.update({f'NO2_lag{j}': df_train['NO2_avg'].iloc[-j]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        elif i == 0:
            for j in range(1, 5):
                if j == 1:
                    row.update({f'PM10_lag{j}': predicted[i][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i][1]})
                    row.update({f'PM1_lag{j}': predicted[i][2]})
                    row.update({f'NO2_lag{j}': predicted[i][3]})
                else:
                    row.update({f'PM10_lag{j}': df_train['PM10_avg'].iloc[-j + 1]})
                    row.update({f'PM2.5_lag{j}': df_train['PM2.5_avg'].iloc[-j + 1]})
                    row.update({f'PM1_lag{j}': df_train['PM1_avg'].iloc[-j + 1]})
                    row.update({f'NO2_lag{j}': df_train['NO2_avg'].iloc[-j + 1]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        elif i == 1:
            for j in range(1, 5):
                if j == 1:
                    row.update({f'PM10_lag{j}': predicted[i][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i][1]})
                    row.update({f'PM1_lag{j}': predicted[i][2]})
                    row.update({f'NO2_lag{j}': predicted[i][3]})
                elif j == 2:
                    row.update({f'PM10_lag{j}': predicted[i - 1][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 1][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 1][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 1][3]})
                else:
                    row.update({f'PM10_lag{j}': df_train['PM10_avg'].iloc[-j + 2]})
                    row.update({f'PM2.5_lag{j}': df_train['PM2.5_avg'].iloc[-j + 2]})
                    row.update({f'PM1_lag{j}': df_train['PM1_avg'].iloc[-j + 2]})
                    row.update({f'NO2_lag{j}': df_train['NO2_avg'].iloc[-j + 2]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        elif i == 2:
            for j in range(1, 5):
                if j == 1:
                    row.update({f'PM10_lag{j}': predicted[i][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i][1]})
                    row.update({f'PM1_lag{j}': predicted[i][2]})
                    row.update({f'NO2_lag{j}': predicted[i][3]})
                elif j == 2:
                    row.update({f'PM10_lag{j}': predicted[i - 1][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 1][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 1][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 1][3]})
                elif j == 3:
                    row.update({f'PM10_lag{j}': predicted[i - 2][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 2][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 2][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 2][3]})
                else:
                    row.update({f'PM10_lag{j}': df_train['PM10_avg'].iloc[-j + 3]})
                    row.update({f'PM2.5_lag{j}': df_train['PM2.5_avg'].iloc[-j + 3]})
                    row.update({f'PM1_lag{j}': df_train['PM1_avg'].iloc[-j + 3]})
                    row.update({f'NO2_lag{j}': df_train['NO2_avg'].iloc[-j + 3]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        elif i == 3:
            for j in range(1, 5):
                if j == 1:
                    row.update({f'PM10_lag{j}': predicted[i][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i][1]})
                    row.update({f'PM1_lag{j}': predicted[i][2]})
                    row.update({f'NO2_lag{j}': predicted[i][3]})
                elif j == 2:
                    row.update({f'PM10_lag{j}': predicted[i - 1][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 1][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 1][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 1][3]})
                elif j == 3:
                    row.update({f'PM10_lag{j}': predicted[i - 2][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 2][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 2][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 2][3]})
                elif j == 4:
                    row.update({f'PM10_lag{j}': predicted[i - 3][0]})
                    row.update({f'PM2.5_lag{j}': predicted[i - 3][1]})
                    row.update({f'PM1_lag{j}': predicted[i - 3][2]})
                    row.update({f'NO2_lag{j}': predicted[i - 3][3]})
                else:
                    row.update({f'PM10_lag{j}': df_train['PM10_avg'].iloc[-j + 4]})
                    row.update({f'PM2.5_lag{j}': df_train['PM2.5_avg'].iloc[-j + 4]})
                    row.update({f'PM1_lag{j}': df_train['PM1_avg'].iloc[-j + 4]})
                    row.update({f'NO2_lag{j}': df_train['NO2_avg'].iloc[-j + 4]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        else:
            for j in range(1, 5):
                row.update({f'PM10_lag{j}': predicted[i - j + 1][0]})
                row.update({f'PM2.5_lag{j}': predicted[i - j + 1][1]})
                row.update({f'PM1_lag{j}': predicted[i - j + 1][2]})
                row.update({f'NO2_lag{j}': predicted[i - j + 1][3]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = rf.predict(values)[0]
            predicted.append(prediction)
        i += 1
    return predicted


def print_mean_values(predicted: list, df_test: pd.DataFrame) -> pd.DataFrame:
    pred_res = pd.DataFrame(columns=['PM10_avg', 'PM2.5_avg', 'PM1_avg', 'NO2_avg'])
    i = 0
    for row in predicted:
        res_dict = {'PM10_avg': row[0], 'PM2.5_avg': row[1], 'PM1_avg': row[2], 'NO2_avg': row[3]}
        res_df = pd.DataFrame(data=res_dict, index=[i])
        pred_res = pd.concat([pred_res, res_df])
        i += 1
    print('Mean averages for predicted values: PM10: ', pred_res['PM10_avg'].mean(), 'PM2.5',
          pred_res['PM2.5_avg'].mean(), 'PM1', pred_res['PM1_avg'].mean(), 'NO2',
          pred_res['NO2_avg'].mean())
    print('Mean averages for real values: PM10: ', df_test['PM10_avg'].mean(), 'PM2.5', df_test['PM2.5_avg'].mean(),
          'PM1', df_test['PM1_avg'].mean(), 'NO2', df_test['NO2_avg'].mean())
    return pred_res


def run_per_hour_prediction():
    data = preprocessing('data_merged.csv')
    X_train, X_test, y_train, y_test, df_train, df_test = split_data(data)
    model = create_model(X_train, y_train)
    with open('model_per_hour.pkl', 'wb') as f:
        pickle.dump(model, f)
    predicted = adjust_lagged_vars_for_y_test(model, df_train, X_test)
    pred_res = print_mean_values(predicted, df_test)
    return pred_res


if __name__ == '__main__':
    pred_res = run_per_hour_prediction()
