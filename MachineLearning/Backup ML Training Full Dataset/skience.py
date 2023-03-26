import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print('hello world!')


data = pd.read_csv('January23.csv')

input_features = ['OM1','OM2','OM3','OM4','OM5','OM6','OM7','OM8','OM9','OM10','OM11','OM12','om_time']
X = data[input_features]
input_labels = ['LASK1','LASK2','LASK3','LASK4','lask_time']
y = data[input_labels]

# Split the data into training and testing sets, and scale the input features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Choose a model and train it
model = LogisticRegression(max_iter=1000,solver='saga')
model.fit(X_train, y_train)





# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate the evaluation metric(s)
accuracy = accuracy_score(y_test, y_pred)

# Print the evaluation metric(s) to the screen
print("Accuracy:", accuracy)
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
