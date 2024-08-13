
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend

import matplotlib.pyplot as plt
import numpy as np

def data_into_chart(max_dices,plot_data):
    for i in range(2, max_dices + 1):
        # Prepare the data for plotting
        x_labels = []
        y_values_0 = []  # Correct Roll
        y_values_1 = []  # Failed Roll
        y_values_2 = []  # Correct Lift
        y_values_3 = []  # Failed Lift
        
        for key1, value1 in plot_data[i].items():
            for key2, value2 in value1.items():
                x_labels.append(f'[{key1},{key2}]')
                y_values_0.append(value2[0])
                y_values_1.append(value2[1])
                y_values_2.append(value2[2])
                y_values_3.append(value2[3])

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))  # Increase figure size

        index = np.arange(len(x_labels))
        bar_width = 0.2  # Adjust bar width for 4 bars per group

        # Define bar positions for each category
        bars1 = ax.bar(index - 1.5 * bar_width, y_values_0, bar_width, label='Correct Roll', color='green')
        bars2 = ax.bar(index - 0.5 * bar_width, y_values_1, bar_width, label='Failed Roll', color='red')
        bars3 = ax.bar(index + 0.5 * bar_width, y_values_2, bar_width, label='Correct Lift', color='blue')
        bars4 = ax.bar(index + 1.5 * bar_width, y_values_3, bar_width, label='Failed Lift', color='orange')

        ax.set_xlabel('X Labels', fontsize=10)  # Adjust font size
        ax.set_ylabel('Values', fontsize=10)  # Adjust font size
        ax.set_title(f'Plot for {i} Dices', fontsize=12)  # Adjust font size
        ax.set_xticks(index)
        ax.set_xticklabels(x_labels, rotation=90, fontsize=8)  # Adjust font size
        ax.legend(fontsize=10)  # Adjust font size

        plt.tight_layout()
        plt.savefig(f'data/plot{i}.png')  # Save the plot as a PNG file
        plt.close()  # Close the plot to avoid displaying it in some environments