import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

# Load the dataset
data = pd.read_csv('January23.csv')

input_features = ['OM1','OM2','OM3','OM4','OM5','OM6','OM7','OM8','OM9','OM10','OM11','OM12','om_time']
X = data[input_features]
input_labels = ['LASK1','LASK2','LASK3','LASK4','lask_time']
y = data[input_labels]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the input features for both training and testing sets
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Load the model from the pickle file
with open('model-mi-mo.pkl', 'rb') as file:
    model = pickle.load(file)

# Predict the outputs using the model
y_pred = model.predict(X_test_scaled)

# Plot the real outputs and predicted outputs for a subset of the test data
num_labels = y_test.shape[1]
subset_size = 100
fig, axes = plt.subplots(num_labels, 1, figsize=(10, 20), sharex=True)

for i in range(num_labels):
    axes[i].plot(y_test.iloc[:subset_size, i], label='Real Output')
    axes[i].plot(y_pred[:subset_size, i], label='Predicted Output')
    axes[i].set_title(f'Label {i+1}')
    axes[i].legend()

fig.text(0.5, 0.04, 'Sample Index', ha='center')
fig.text(0.04, 0.5, 'Output Value', va='center', rotation='vertical')
plt.suptitle(f'Real vs. Predicted Outputs for {subset_size} Test Data Samples')
plt.show()
