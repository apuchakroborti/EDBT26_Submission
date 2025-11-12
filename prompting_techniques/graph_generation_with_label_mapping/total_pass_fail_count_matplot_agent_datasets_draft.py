"""
Below is a Python code to generate a bar graph with three categories. Each category has two bars (with helper and without helper), 
and each bar is divided into two portions (pass and fail). The "pass" portion is green, and the "fail" portion is red. Additionally, each bar is distinguishable separately.

### Python Code:
```python
"""
import matplotlib.pyplot as plt
import numpy as np

# Sample data
categories = ['magicoder', 'deepseek-coder-v2', 'llama3:70b']

with_corrector = {'Pass': [3, 7, 7], 'Fail': [8, 4, 4]}
without_corrector = {'Pass': [1, 2, 2], 'Fail': [10, 9, 9]}


# Number of categories
n_categories = len(categories)

# Bar width and positions
bar_width = 0.35
x = np.arange(n_categories)

# Plot bars for "With Helper"
plt.bar(x - bar_width/2, without_corrector['Pass'], width=bar_width, label='Without Corrector - Pass', color='green', edgecolor='black')
plt.bar(x - bar_width/2, without_corrector['Fail'], width=bar_width, bottom=without_corrector['Pass'], label='Without Corrector - Fail', color='red', edgecolor='black')

# Plot bars for "Without Helper"
plt.bar(x + bar_width/2, with_corrector['Pass'], width=bar_width, label='With Corrector - Pass', color='green', hatch='//', edgecolor='black')
plt.bar(x + bar_width/2, with_corrector['Fail'], width=bar_width, bottom=with_corrector['Pass'], label='With Corrector - Fail', color='red', hatch='//', edgecolor='black')

# Add category labels
plt.xticks(x, categories)

# Add labels and title
plt.xlabel('LLM models')
plt.ylabel('Number of Evaluated Python Scripts')
plt.title('Evaluation of Generated Code for the FAST_MRI_BRAIN Datasets')
plt.legend(loc='upper left')

# Add grid for better visibility
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

"""```

### Explanation:
1. **Data Structure**: 
   - `with_helper` and `without_helper` contain counts for "Pass" and "Fail" portions for each category.
   - Each key (`Pass` and `Fail`) holds a list of values for the three categories.

2. **Stacked Bars**:
   - Bars are plotted for "Pass" using `plt.bar()`.
   - "Fail" values are stacked using the `bottom` parameter.

3. **Distinct Bars**:
   - Bars for "With Helper" are on the left (`x - bar_width/2`), and bars for "Without Helper" are on the right (`x + bar_width/2`).
   - Hatch patterns (`hatch='//'`) are used to differentiate "Without Helper" visually.

4. **Colors**:
   - "Pass" is green, and "Fail" is red for all bars.

5. **Legend and Labels**:
   - A legend is added for clarity.
   - `plt.xticks()` is used to label the categories.

6. **Grid**:
   - A horizontal grid improves readability.

Let me know if you need further adjustments!
"""