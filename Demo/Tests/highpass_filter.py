import numpy as np
from scipy.signal import butter, filtfilt

# Your raw sensor data (replace with your actual data)
data = np.array([4000, 4005, 4010, 4005, 5000, 4995, 4990, 4995])

# Define the filter parameters
cutoff_frequency = 0.1  # Choose a cutoff frequency (in Hz)
sampling_rate = 100  # Adjust the sampling rate of your data (in Hz)
filter_order = 1  # First-order Butterworth filter

# Design the high-pass filter
nyquist_frequency = 0.5 * sampling_rate
normalized_cutoff_frequency = cutoff_frequency / nyquist_frequency
b, a = butter(filter_order, normalized_cutoff_frequency, btype='high', analog=False)

# Apply the high-pass filter to the data
filtered_data = filtfilt(b, a, data)

print("Raw data: ", data)
print("Filtered data: ", filtered_data)
