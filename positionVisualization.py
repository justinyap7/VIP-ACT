import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the first Excel file (positions)
filename_positions = "position.xlsx"
data_positions = pd.read_excel(filename_positions, engine='openpyxl')

# Load the second Excel file (for coloring)
filename_velocities = "velocty.xlsx"
data_velocities = pd.read_excel(filename_velocities, engine='openpyxl')

# Compute min, mean, and max of the velocity data
min_velocity = data_velocities.values.min()
mean_velocity = data_velocities.values.mean()
max_velocity = data_velocities.values.max()

fig, ax = plt.subplots(figsize=(10, 8))

# Define the value ranges and colors based on the computed values
nodes = [min_velocity, mean_velocity, max_velocity]
colors = ["red", "yellow", "green"]

# Normalize the color nodes between 0 and 1
nodes_normalized = [(val - nodes[0]) / (nodes[-1] - nodes[0]) for val in nodes]
cmap = plt.cm.colors.LinearSegmentedColormap.from_list("custom_colormap", list(zip(nodes_normalized, colors)), N=256)

# Set the x-axis as time
times = [(i+1) * 0.01 for i in range(data_positions.shape[1])]

# Plot each car's position from the Postions with colors based on the velocities 
for index, row in data_positions.iterrows():
    for col_index, position in enumerate(row):
        velocity_value = data_velocities.iloc[index, col_index]
        normalized_velocity = (velocity_value - nodes[0]) / (nodes[-1] - nodes[0])
        
        color = cmap(normalized_velocity)
        
        if col_index < len(row) - 1:
            plt.fill_between([times[col_index], times[col_index + 1]], [position, row[col_index + 1]], color=color, alpha=0.5)
            
# Dummy object for colorbar creation
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=nodes[0], vmax=nodes[-1]))
sm.set_array([])  # This line has to be here for the code to work with newer versions of matplotlib
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Velocity Value', rotation=270, labelpad=15)

plt.xlabel('Time (seconds)')
plt.ylabel('Position')
plt.title('Position of Cars over Time')
plt.grid(True)
plt.show()