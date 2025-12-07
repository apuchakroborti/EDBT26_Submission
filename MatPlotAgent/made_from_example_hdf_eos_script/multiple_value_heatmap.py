import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Replace these with your actual time and pressure data
time = np.linspace(0, 100, 12)  # Example time data (12 values)
pressure = np.linspace(0, 50, 10)  # Example pressure data (10 values)
data = np.random.rand(10, 12)  # Replace with actual data matching the shape of time and pressure
print('Shape of time: ', time.shape)
print('Shape of pressure: ', pressure.shape)
print('Shape of data: ', data.shape)


# Create a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=True, cmap='viridis', xticklabels=time, yticklabels=pressure)

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Pressure')
plt.title('Heatmap of Time vs Pressure')

# Show the plot
plt.show()
