import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def prepare_data(df, forecast_col, forecast_out, test_size):
    label = df[forecast_col].shift(-forecast_out)
    x = np.array(df[[forecast_col]])
    x = preprocessing.scale(x)
    x_Lately = x[-forecast_out:]
    x = x[:-forecast_out]
    label.dropna(inplace = True)
    y = np.array(label)
    x_Train, x_Test, y_Train, y_Test = train_test_split(x, y, test_size=test_size, random_state=0)

    response = [x_Train, x_Test, y_Train, y_Test, x_Lately]
    return response

df = pd.read_csv("prices.csv")
print(df)

forecast_col = "Close"
forecast_out = 5
test_size = 0.2

x_Train, x_Test, y_Train, y_Test, x_Lately = prepare_data(df, forecast_col, forecast_out, test_size)
learner = LinearRegression()

learner.fit(x_Train, y_Train)

score = learner.score(x_Test, y_Test)
forecast = learner.predict(x_Lately)
response = {}
response['test_score'] = score
response['forecast_set'] = forecast

print(response)