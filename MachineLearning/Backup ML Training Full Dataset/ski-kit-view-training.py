import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
loaded_model = False

print('hello world!')


data = pd.read_csv('January23.csv')

input_features = ['OM1','OM2','OM3','OM4','OM5','OM6','OM7','OM8','OM9','OM10','OM11','OM12']
X = data[input_features]
y = data['LASK1']

# Split the data into training and testing sets, and scale the input features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize the SGDClassifier
model = SGDClassifier(loss='log', max_iter=1, tol=None, random_state=42, warm_start=True, learning_rate='adaptive', eta0=0.01)

# Load the saved model from the file
with open('model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Train the model with partial_fit and monitor progress
if not loaded_model:
    num_epochs = 100
    for epoch in range(num_epochs):
        model.partial_fit(X_train, y_train, classes=np.unique(y))
        train_accuracy = accuracy_score(y_train, model.predict(X_train))
        print(f"Epoch {epoch + 1}/{num_epochs}, Training Accuracy: {train_accuracy:.4f}")

# Save the trained model to a file
#with open('model.pkl', 'wb') as f:
#    pickle.dump(model, f)

# Make predictions on the test data
y_pred = loaded_model.predict(X_test)

# Calculate the evaluation metric(s)

accuracy = accuracy_score(y_test, y_pred)


    
# Print the evaluation metric(s) to the screen
print("Test Accuracy:", accuracy)
