import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import splrep, splev
import scipy.integrate as spi
from scipy.spatial.distance import euclidean

st.set_page_config(
    page_title="Stream Discharge",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Columns
col1, col2, col3 = st.columns(spec=[0.40,0.20,0.40], gap = "large")

with col1:
    df = pd.DataFrame(
        [
        {"Distance Traversed": 0, "Relative Elevation": 100.0},
        {"Distance Traversed": 5, "Relative Elevation": 98.0},
        {"Distance Traversed": 10, "Relative Elevation": 96.0},
        {"Distance Traversed": 15, "Relative Elevation": 98.0},
        {"Distance Traversed": 20, "Relative Elevation": 100.0},
    ]
    )

    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    edited_df.dropna(inplace=True)

with col2:
    if edited_df.shape[0] == 0 or edited_df['Distance Traversed'].duplicated().any():
        st.error("Check the datatable, it is either **Empty** or has duplicates in **Distance Traversed** column", icon="🚨")
    else:
        # Declaration of variables
        x = edited_df["Distance Traversed"].values
        y = edited_df["Relative Elevation"].values

        # Reshaping y data setting minimum y as 0
        min_y = np.min(y)
        y = y - min_y

        # Calculate spline representation of the data
        tck = splrep(x, y)

        # Generate points on the spline curve for a smoother line
        pointsPerMeter = 100
        add_points = int(np.max(x)*pointsPerMeter)
        x_additional = np.linspace(np.min(x), np.max(x), add_points+1)
        y_additional = splev(x_additional, tck)

        sorted_indices = np.argsort(x_additional)
        x_additional = x_additional[sorted_indices]
        y_additional = y_additional[sorted_indices]

        # Define the y-value up to which filling should be shown
        fill_y = st.number_input('Enter the depth of water')

        # Create a figure and axes object
        fig, ax = plt.subplots()

        ax.plot(x_additional, y_additional)
        ax.fill_between(x_additional, y_additional, fill_y, where=(y_additional <= fill_y), color='skyblue', alpha=0.8)
        ax.scatter(x, y, color='red')
        ax.set_xlabel('Chainage')
        ax.set_ylabel('Relative height')
        ax.set_title('Smoothed Line Plot with Filling')
        ax.grid(True)

        col3.pyplot(fig)

        if fill_y>0:
            def calculate_total_distance(x_coordinates, y_coordinates):
                total_distance = 0.00
                # Combine x and y coordinates into a single array
                coordinates = np.column_stack((x_coordinates, y_coordinates))
                # Iterate over the sequential coordinates
                for i in range(len(coordinates) - 1):
                    # Calculate the distance between consecutive points
                    if int((coordinates[i+1][0]-coordinates[i][0])*pointsPerMeter) <= pointsPerMeter:
                        distance = euclidean(coordinates[i], coordinates[i+1])
                        total_distance += distance
                    else:
                        print(f"Interval disrupted at {coordinates[i][0]}")
                return total_distance
            
            # Filter the coordinates based on the fill_y condition
            filtered_indices = np.where(y_additional <= fill_y)[0]
            x_filter = x_additional[filtered_indices]
            y_filter = y_additional[filtered_indices]

            # Calculate the area under the curve using Simpson's rule
            area_1 = spi.trapezoid(y_filter, x_filter)

            # Calculate total area above and below curve
            area_2 = (np.max(y_filter)-np.min(y_filter))*(np.max(x_filter)-np.min(x_filter))

            # Calculate area above the curve
            area_3 = area_2-area_1

            st.write("Total area is", area_2)
            st.write("The area under curve is ", area_1)
            st.write("Area above curve is",area_3)

            coordinates = np.column_stack((x_filter, y_filter))

            length = calculate_total_distance(x_filter, y_filter)

            n=0.04
            s=1/1000

            if n!=0 and length!=0:
                v = (1/n)*((area_3/length)**(2/3))*((s)**(1/2))
                q = area_3*v
                st.write(f"The length of the curve is: {length:.2f}")
                st.write(f"Velocity is {v}")
                st.write(f"Discharge is {q}")
