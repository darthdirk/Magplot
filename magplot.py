import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the CSV data specifying that there are no headers

csv_path1 = '~/01.17.20241.csv'
csv_path2 = '~/01.17.20242.csv'
csv_path3 = '~/01.17.20243.csv'

def process_csv(csv_path):
    # Calculate the phase in degrees and magnitude of the complex numbers
    data = pd.read_csv(csv_path, header=None, names=['Frequency', 'Real', 'Imaginary'])
    data['Phase'] = np.angle(data['Real'] + 1j * data['Imaginary'], deg=True)
    data['Magnitude'] = np.abs(data['Real'] +1j * data['Imaginary'])
    return data

# Process bolth CSV files
data1 = process_csv(csv_path1)
data2 = process_csv(csv_path2)
data3 = process_csv(csv_path3)

# Plotting the graph
fig, ax1 = plt.subplots()

# Plot the first CSV
color = 'tab:red'
ax1.set_xlabel('Frequency (MHz)')
ax1.set_ylabel('Phase (deg)', color=color)
ax1.plot(data1['Frequency'], data1['Phase'], color=color, label= f'Phase SN1')
ax1.tick_params(axis='y', labelcolor=color)

# Plot for the second CSV on the same axis
color = 'tab:green'
ax1.plot(data2['Frequency'], data2['Phase'], color=color, linestyle='--', label= f'Phase SN2')
ax1.legend(loc='upper left')

# Plot the third CSV on the same axis
color = 'tab:brown'
ax1.plot(data3['Frequency'], data3['Phase'], color=color, label= f'Phase SN3')
ax1.legend(loc='upper left')

# Instantiate a second axes that shares the same x-axis for Mag
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Gain Magnitude', color=color)
ax2.plot(data1['Frequency'], data1['Magnitude'], color=color, label= f'Magnitude SN1')
ax2.tick_params(axis='y', labelcolor=color)

# Plot for the second CSV on the secondary y-axis
color = 'tab:orange'
ax2.plot(data2['Frequency'], data2['Magnitude'], color=color, linestyle='--', label= f'Magnitude SN2')
ax2.legend(loc='upper right')

# Plot for the third CSV on the secondary y-axis
color = 'tab:purple'
ax2.plot(data3['Frequency'], data3['Magnitude'], color=color, label= f'Magnitude SN3')
ax2.legend(loc='upper right')

# Set the title of the graph to the CSV file name
plt.title(f'Overlay Graph for {csv_path1.split("/")[-1]} and {csv_path2.split("/")[-1]}')

# Otherwise the right y-label is slightly clipped
fig.tight_layout()

# Display the plot
plt.show()
