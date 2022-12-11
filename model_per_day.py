import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings
import xgboost
import numpy as np
from yellowbrick.regressor import ResidualsPlot
from sklearn.metrics import mean_squared_error as MSE
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import pickle


warnings.filterwarnings(action='ignore')


def group_weather(weather_df: pd.DataFrame) -> pd.DataFrame:
    return weather_df.groupby('date').agg(
        max_temp=('temp', np.max),
        min_temp=('temp', np.min),
        pressure_avg=('surface_pressure', np.mean),
        windspeed_max=('windspeed_10m', np.max),
        windspeed_min=('windspeed_10m', np.min),
        winddir_avg=('winddirection_10m', np.mean),
        precipitation_sum=('precipitation', np.sum)).reset_index()


def preprocessing(weather_path: str, smog_path: str) -> pd.DataFrame:
    weather_df = pd.read_csv(weather_path)
    smog_df = pd.read_csv(smog_path, names=['date', 'PM10', 'none'], skiprows=1).drop(columns=['none'])
    weather_df = weather_df.rename(columns={'temperature_2m': 'temp'})
    weather_df['time'] = weather_df.apply(lambda x: x['time'].split('T')[0], axis=1)
    weather_df['time'] = pd.to_datetime(weather_df['time'])
    weather_df = weather_df.rename(columns={'time': 'date'})
    weather_df = group_weather(weather_df)
    smog_df['date'] = pd.to_datetime(smog_df['date'])
    weather_df['date'] = weather_df.apply(lambda x: str(x['date']), axis=1)
    smog_df['date'] = smog_df.apply(lambda x: str(x['date']), axis=1)
    return weather_df.merge(smog_df, on='date')


def add_lagged_variables(df: pd.DataFrame, cols: list, start: int, end: int) -> pd.DataFrame:
    for col in cols:
        for i in range(start, end):
            df[f'{col}{i}'] = df[f'{col}'].shift(i)
    return df


def run_model_training(df: pd.DataFrame, verbose=True):
    df = df.dropna()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = []
    rmse = []
    rmse_rf = []
    scores_rf = []
    y = df['PM10']
    X = df.drop(columns=['PM10', 'date'])
    i = 0
    rf = RandomForestRegressor(random_state=42)
    xg = xgboost.XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8,
                              random_state=42)
    for train, test in kf.split(X, y):
        print(f'Fold:{i}, Train set: {len(train)}, Test set:{len(test)}')
        feature_names = [f"{col}" for col in X.columns]
        y_train = y.iloc[train]
        X_train = X.iloc[train]
        y_test = y.iloc[test]
        X_test = X.iloc[test]
        xg.fit(X_train, y_train)
        pred = xg.predict(X_test)
        rmse.append(np.sqrt(MSE(y_test, pred)))
        scores.append(xg.score(X_test, y_test))
        rf.fit(X_train, y_train)
        importances = rf.feature_importances_
        std = np.std([rf.feature_importances_ for tree in rf.estimators_], axis=0)
        scores_rf.append(rf.score(X_test, y_test))
        pred_rf = rf.predict(X_test)
        rmse_rf.append(np.sqrt(MSE(y_test, pred_rf)))
        if verbose:
            forest_importances = pd.Series(importances, index=feature_names)
            fig, ax = plt.subplots()
            forest_importances.plot.bar(yerr=std, ax=ax)
            ax.set_title("Feature importances using MDI")
            ax.set_ylabel("Mean decrease in impurity")
            fig.tight_layout()
            plt.show()
            visualizer_xg = ResidualsPlot(xg)
            visualizer_xg.fit(X_train, y_train)  # Fit the training data to the visualizer
            visualizer_xg.score(X_test, y_test)  # Evaluate the model on the test data
            visualizer_xg.show()  # Finalize and render the figure
            visualizer_rf = ResidualsPlot(rf)
            visualizer_rf.fit(X_train, y_train)  # Fit the training data to the visualizer
            visualizer_rf.score(X_test, y_test)  # Evaluate the model on the test data
            visualizer_rf.show()  # Finalize and render the figure
        i += 1
    print(sum(scores)/len(scores))
    print(sum(scores_rf)/len(scores_rf))
    print(sum(rmse)/len(rmse))
    print(sum(rmse_rf)/len(rmse_rf))
    if sum(scores)/len(scores) > sum(scores_rf)/len(scores_rf):
        return xg
    else:
        return rf


def run_model() -> pd.DataFrame:
    data = preprocessing('era5 (5).csv', 'gios-pjp-data.csv')
    data = add_lagged_variables(data, ['PM10'], 1, 2)
    model = run_model_training(data)
    with open('model_24h/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    return data


if __name__ == '__main__':
    data = run_model()
