import numpy as np
import pandas as pd
import pickle
from model_per_day import run_model


def create_dummy_weather_data() -> pd.DataFrame:
    prediction_dummy = pd.DataFrame(data={'date': ['2022-12-04', '2022-12-05', '2022-12-06'], 'max_temp': [0.6, 0.8, 0.4], 'min_temp': [-1.3, -1.6, -1.2], 'pressure_avg': [1002, 997, 1025], 'windspeed_max': [30, 25, 12], 'windspeed_min': [15, 13, 8], 'winddir_avg': [250, 280, 90], 'precipitation_sum': [0.0, 0.5, 1.2]})
    prediction_dummy['date'] = pd.to_datetime(prediction_dummy['date'])
    return prediction_dummy


def run_prediction_mechanism(prediction_dummy: pd.DataFrame) -> list:
    data = run_model()
    with open('model_24h/model.pkl', 'rb') as f:
        model = pickle.load(f)
    predicted = []
    i = -1
    prediction_dummy_no_date = prediction_dummy.drop(columns=['date'])
    for row in prediction_dummy_no_date.to_dict(orient='records'):
        if i == -1:
            row.update({'PM10_lag1': data['PM10'].iloc[-1]})
            values = np.array(list(row.values())).reshape(1, -1)
            prediction = model.predict(values)[0]
            predicted.append(prediction)
            print(row)
            print(prediction)
        else:
            row.update({'PM10_lag1': predicted[i]})
            values = np.array(list(row.values())).reshape(1, -1)
            print(row)
            prediction = model.predict(values)[0]
            predicted.append(prediction)
            print(prediction)
        i += 1
    return predicted


def prepare_results(prediction_dummy: pd.DataFrame, predicted: list) -> pd.DataFrame:
    results = {prediction_dummy['date'].iloc[i]: [predicted[i]] for i in range(len(predicted))}
    print(results)
    results = pd.DataFrame(data=results).transpose()
    results.columns = ['PM10']
    return results


def classify_pm10_level(results: pd.DataFrame):
    results['PM10_level'] = np.select([results['PM10'] < 20, results['PM10'] > 50], [0, 2], default=1)
    return results


def save_predictions_to_parquet(results: pd.DataFrame):
    results.to_parquet('predictions/dummy_predictions.parquet')


def run():
    dummy_df = create_dummy_weather_data()
    predicted = run_prediction_mechanism(dummy_df)
    results = prepare_results(dummy_df, predicted)
    results = classify_pm10_level(results)
    save_predictions_to_parquet(results)


if __name__ == '__main__':
    run()
