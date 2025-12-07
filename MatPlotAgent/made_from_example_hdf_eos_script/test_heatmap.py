import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Sample scientific data (2D array)
data = np.random.rand(10, 12)  # Replace this with your own scientific data
print(data)

# Create a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=True, cmap='viridis')

# Add labels and a title
plt.xlabel('X axis label (e.g., Time)')
plt.ylabel('Y axis label (e.g., Pressure)')
plt.title('Heatmap of Scientific Data')

# Show the plot
plt.show()
