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

print('hello world!')

    
def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    

data = pd.read_csv('Data-Captures/capture_010.csv')

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
with open('Trained-Demo-NoTime-April23.pkl', 'wb') as f:
    pickle.dump(model, f)


# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
evaluate_model(y_test, y_pred)

# Create a new DataFrame with the actual and predicted labels
result_df = y_test.copy().reset_index(drop=True)
result_df.columns = ['Actual LASK1', 'Actual LASK2', 'Actual LASK3', 'Actual LASK4']
result_df['Predicted LASK1'] = y_pred[:, 0]
result_df['Predicted LASK2'] = y_pred[:, 1]
result_df['Predicted LASK3'] = y_pred[:, 2]
result_df['Predicted LASK4'] = y_pred[:, 3]

# Save the DataFrame as a CSV file
result_df.to_csv('avp-4-2-23.csv', index=False)

