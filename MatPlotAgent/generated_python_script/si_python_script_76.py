import pandas as pd
import matplotlib.pyplot as plt
import h5py

# Load the HDF5 file
file_path = '/Users/apukumarchakroborti/gsu_research/llam_test/plot_generation/csv_to_h5_data/76_h5_data.h5'
data = h5py.File(file_path, 'r')

# Extract the "Women's millions of dollars" column
women_column = data['Women\'s millions of dollars'][:]

# Convert to a DataFrame for easier handling if needed
df = pd.DataFrame(women_column, columns=['Women\'s millions of dollars'])

# Plotting
fig, ax_box = plt.subplots()
fig.set_size_inches(10, 6)

# Box plot
bp = ax_box.boxplot(df['Women\'s millions of dollars'], vert=True, patch_artist=True, notch=False)
ax_box.set_ylabel('Values')
ax_box.set_title('Box Plot and Histogram of "Women\'s millions of dollars"')

# Highlight quartiles with continuous red dashed lines
for box in bp['boxes']:
    box.set(color='black', linewidth=1)
    if 'outliers' in bp:
        del bp['outliers']

# Histogram
ax_hist = fig.add_subplot(2, 1, 2)
n, bins, patches = ax_hist.hist(df['Women\'s millions of dollars'], bins='auto', edgecolor='black')
ax_hist.set_xlabel('Values')
ax_hist.set_ylabel('Frequency')

# Label key statistics on the box plot
stats = df['Women\'s millions of dollars'].describe()
median = stats['50%']
q1 = stats['25%']
q3 = stats['75%']
ax_box.text(1.1, median, f'Median: {median:.2f}', verticalalignment='center')
ax_box.text(1.1, q1, f'Q1: {q1:.2f}', verticalalignment='center')
ax_box.text(1.1, q3, f'Q3: {q3:.2f}', verticalalignment='center')

# Detail the frequency distribution in the histogram
ax_hist.set_title('Histogram of "Women\'s millions of dollars"')

plt.tight_layout()
plt.show()
