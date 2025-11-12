"""The `matplotlib.pyplot` library in Python is used for creating visualizations such as plots, graphs, and charts. Here are examples of how to use it for various cases:

### 1. **Basic Line Plot**
```python
"""
import matplotlib.pyplot as plt

# Example data
x = [0, 1, 2, 3, 4]
y = [0, 2, 4, 6, 8]

# Create line plot
plt.plot(x, y)
plt.title('Basic Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

"""```

### 2. **Scatter Plot**
```python
"""
import matplotlib.pyplot as plt

# Example data
x = [5, 10, 15, 20, 25]
y = [2, 3, 4, 5, 6]

# Create scatter plot
plt.scatter(x, y)
plt.title('Scatter Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

"""```

### 3. **Bar Plot**
```python
"""
import matplotlib.pyplot as plt

# Example data
categories = ['A', 'B', 'C', 'D']
values = [5, 7, 3, 8]

# Create bar plot
plt.bar(categories, values)
plt.title('Bar Plot')
plt.ylabel('Values')
plt.show()

"""```

### 4. **Histogram**
```python
"""
import matplotlib.pyplot as plt
import numpy as np

# Example data
data = np.random.randn(1000)

# Create histogram
plt.hist(data, bins=30)
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

"""```

### 5. **Pie Chart**
```python
"""

import matplotlib.pyplot as plt

# Example data
labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
sizes = [15, 30, 45, 10]

# Create pie chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Pie Chart')
plt.show()

"""```

### 6. **Subplots (Multiple Plots in One Figure)**
```python
"""
import matplotlib.pyplot as plt

# Data for subplots
x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [5, 10, 15, 20, 25]

# Create subplots
plt.subplot(1, 2, 1)
plt.plot(x, y1, 'r')  # Red line plot
plt.title('Square Numbers')

plt.subplot(1, 2, 2)
plt.plot(x, y2, 'g')  # Green line plot
plt.title('Linear Numbers')

plt.tight_layout()
plt.show()


"""```

### 7. **Customization: Line Styles, Colors, Markers**
```python
"""

import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create plot with customized line style, color, and marker
plt.plot(x, y, linestyle='--', color='r', marker='o')
plt.title('Customized Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

"""```

### 8. **Adding Annotations**
```python
"""

import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create plot
plt.plot(x, y)
plt.title('Annotated Plot')

# Add annotation
plt.annotate('Max Point', xy=(5, 10), xytext=(3, 9),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.show()

"""```

### 9. **Logarithmic Scale**
```python
"""
import matplotlib.pyplot as plt

# Example data
x = [1, 10, 100, 1000, 10000]
y = [1, 10, 100, 1000, 10000]

# Create plot with logarithmic scale
plt.plot(x, y)
plt.xscale('log')
plt.yscale('log')
plt.title('Logarithmic Scale Plot')
plt.xlabel('Log X-axis')
plt.ylabel('Log Y-axis')
plt.show()

"""```

### 10. **Saving Figures**
```python
"""

import matplotlib.pyplot as plt

# Example data
x = [0, 1, 2, 3, 4]
y = [0, 2, 4, 6, 8]

# Create line plot
plt.plot(x, y)
plt.title('Saving a Plot')

# Save the figure to a file
plt.savefig('saved_plot.png')

# Show the plot
plt.show()

"""```

### 11. **Heatmap**
```python
"""
import matplotlib.pyplot as plt
import numpy as np

# Example data
data = np.random.rand(10, 10)

# Create heatmap
plt.imshow(data, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Heatmap')
plt.show()

"""```

### 12. **3D Plot (using `mpl_toolkits.mplot3d`)**
```python
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Example data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

plt.title('3D Surface Plot')
plt.show()

"""```

These examples cover a wide range of use cases for `matplotlib.pyplot` in Python, from simple plots to advanced 3D and heatmap visualizations. You can extend and customize them further based on your specific requirements.
"""