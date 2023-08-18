import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    
datafile = 'capture_11.csv'
data = pd.read_csv(f'Data-Captures/{datafile}')

print(f'Training Model from {datafile}')

input_features = ['OM1','OM2','OM3','OM4','OM5','OM6','OM7','OM8','OM9','OM10','OM11','OM12','om_time']
X = data[input_features]
input_labels = ['LASK1','LASK2','LASK3','LASK4','lask_time']
y = data[input_labels]

# Split the data into training and testing sets, and scale the input features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()


base_model = RandomForestRegressor(n_estimators=100, random_state=42)

model = MultiOutputRegressor(base_model)

model.fit(X_train, y_train)

# Print the evaluation metric(s) to the screen
with open(f'{datafile.split(".")[0]}.pkl', 'wb') as f:
    pickle.dump(model, f)


# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
evaluate_model(y_test, y_pred)


