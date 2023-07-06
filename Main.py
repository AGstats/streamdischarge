import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import splrep, splev
import scipy.integrate as spi
from scipy.spatial.distance import euclidean

st.set_page_config(
    page_title="SF Discharge Main",
    page_icon=":ocean:",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("""**:violet[Need for this App]  :thought_balloon:**  
        Stream Cross-Sections are irregular in shape and highly dynamic in nature which makes manual calculation of Wetted area and Wetted perimeter with fluctuation of water depth a tedious task.  
        \n  This App is intended to Simplify this task by making use of Interpolation Techniques and Numerical Methods in Python.  
        """)
    st.divider()
    st.markdown("""Developed and Maintained by     
            :sparkles: :sparkles: **:green[Ashok Guntu]** :sparkles: :sparkles: 
            """)
    st.divider()
    st.markdown("""**:blue[Credits]**  
                This App is coded in Python using these popular Open Source libraries  
                :star2: **[Pandas](https://pandas.pydata.org)**    
                :star2: **[NumPy](https://numpy.org)**    
                :star2: **[SciPy](https://scipy.org)**    
                :star2: **[Matplotlib](https://matplotlib.org)**   
                :star2: **[Streamlit](https://streamlit.io)**  
                """)

# Columns
col1, col2, col3 = st.columns(spec=[0.30, 0.30, 0.40], gap="large")

if "inputsentered" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [
            {"Distance": 0.0, "Elevation": 100.00},
            {"Distance": 5.0, "Elevation": 98.00},
            {"Distance": 10.0, "Elevation": 96.00},
            {"Distance": 15.0, "Elevation": 98.00},
            {"Distance": 20.0, "Elevation": 100.00},
        ]
    )
    st.session_state.fixeddf= st.session_state.df.copy()
    st.session_state.edit_df= st.session_state.df.copy()
    st.session_state.editmode = True
    st.session_state.b1visibility = True
    st.session_state.b2visibility = False
    st.session_state.b3visibility = False
    st.session_state.b4visibility = False
    st.session_state.inputsentry = False
    st.session_state.inputsentered = False

def turnoffeditmode():
    st.session_state.editmode = False
    st.session_state.b1visibility = False
    st.session_state.b2visibility = True
    st.session_state.fixeddf = st.session_state.edit_df.copy()
    st.session_state.fixeddf.dropna(inplace=True)

def proceedfurther():
    st.session_state.inputsentry = True
    st.session_state.b2visibility = False
    st.session_state.b3visibility = True

def runcomputations():
    st.session_state.inputsentered = True
    st.session_state.b3visibility = False

def clearsessionstate():
    st.cache_data.clear()
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]

fill_y = None
n = None
s = None

if st.session_state.b1visibility:
    col3.button(":chart_with_upwards_trend: PLOT", on_click=turnoffeditmode)

if st.session_state.b2visibility:
    col3.button(":keyboard: ENTER INPUTS", on_click=proceedfurther)

if st.session_state.b3visibility:
    col3.button(":computer: COMPUTE", on_click=runcomputations)

if not st.session_state.editmode:
    col1.button(":pencil: REFRESH", on_click=clearsessionstate)

edited_df = st.session_state.fixeddf

st.session_state.edit_df = col1.data_editor(
    edited_df,
    num_rows="dynamic" if st.session_state.editmode else "fixed",
    disabled=False if st.session_state.editmode else True,
    use_container_width=True,
    hide_index=True,
    key="edited_table",
)

if st.session_state.editmode:
    col2.info(
        """ :keyboard: The table displayed here is a dynamic table with pre-populated cross-section data.  
        \n  :star: Please fill the table and then click on **:green[PLOT]** button to plot the cross-section. :chart_with_upwards_trend:
        \n  :star: The rows are dynamic and can be added based on requirement using :heavy_plus_sign: icon at the bottom.    
        \n  :star: Alternatively data can be copied from excel or other external sources and be pasted into this table for more ease. :sparkles:  
        \n  :star: Make sure that there are no duplicates in distance column and atleast :four: rows of data is entered.  
        \n  :star: If you just want to explore the App, then feel free to go ahead :dash: with the sample data for a quick overview of the App. :rocket:  
    """)
elif edited_df.shape[0] < 4 or edited_df["Distance"].duplicated().any():
    col2.error(
        "Check the Data Table, it either doesn't have minimum number of rows (**Atleast 4 Rows**) or has duplicates in **Distance** column",
        icon="🚨",
    )
else:

    @st.cache_data
    def interpolate_curve(edited_df, pointsPerMeter=100):
        # Declaration of variables
        x = edited_df["Distance"].values
        y = edited_df["Elevation"].values

        # Reshaping y data setting minimum y as 0
        min_y = np.min(y)
        y = y - min_y

        sorted_indices = np.argsort(x)
        x = x[sorted_indices]
        y = y[sorted_indices]

        # Calculate spline representation of the data
        tck = splrep(x, y, per=0)

        # Generate points on the spline curve for a smoother line
        add_points = int(np.max(x) * pointsPerMeter)
        x_additional = np.linspace(np.min(x), np.max(x), add_points + 1)
        y_additional = splev(x_additional, tck)

        sorted_indices = np.argsort(x_additional)
        x_additional = x_additional[sorted_indices]
        y_additional = y_additional[sorted_indices]
        return x, y, x_additional, y_additional

    pointsPerMeter = 100
    x, y, x_additional, y_additional = interpolate_curve(edited_df, pointsPerMeter)

    if st.session_state.inputsentry:
        fill_y = col2.number_input("**:violet[Enter the Depth of Water Column in Meters]**", value=0.00, min_value=0.00, max_value=max(y), step=0.10)
        n = col2.number_input(
            "**:violet[Enter Mannings Coefficient]**", value=0.030, min_value=0.001, max_value=0.100, step=0.005, format="%.3f"
        )
        s = col2.number_input(
            "**:violet[Enter Longitudinal Slope]**  \n (units of fall for 1000 units run)",
            value=1.00,
            min_value=0.01,
            max_value=999.00,
            step=0.05,
        )

    # Create a figure and axes object
    fig, ax = plt.subplots()
    if fill_y is None:
        fill_y = 0.00
    ax.plot(x_additional, y_additional)
    ax.fill_between(
        x_additional,
        y_additional,
        fill_y,
        where=(y_additional <= fill_y),
        color="skyblue",
        alpha=0.8,
    )
    ax.scatter(x, y, color="red")
    ax.set_xlabel("Distance")
    ax.set_ylabel("Elevation")
    ax.set_title("Smoothed Line Plot")
    ax.grid(True)

    col3.pyplot(fig)

    if st.session_state.inputsentered and fill_y > 0.001:
        col2.info("You may now change any of the Input Parameters :1234: and observe Live Results")
        col2.success("""Refer this website for Mannings Coefficient  
                     [Click Here](https://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm)""")
        @st.cache_data
        def calculate_total_distance(x_filter, y_filter):
            # Calculate the area under the curve using Simpson's rule
            area_1 = spi.trapezoid(y_filter, x_filter)

            # Calculate total area above and below curve
            area_2 = (np.max(y_filter) - np.min(y_filter)) * (
                np.max(x_filter) - np.min(x_filter)
            )

            # Calculate area above the curve
            area_3 = area_2 - area_1

            total_distance = 0.00
            # Combine x and y coordinates into a single array
            coordinates = np.column_stack((x_filter, y_filter))
            # Iterate over the sequential coordinates
            for i in range(len(coordinates) - 1):
                # Calculate the distance between consecutive points
                if (
                    int((coordinates[i + 1][0] - coordinates[i][0]) * pointsPerMeter)
                    <= pointsPerMeter
                ):
                    distance = euclidean(coordinates[i], coordinates[i + 1])
                    total_distance += distance
                else:
                    print(f"Interval disrupted at {coordinates[i][0]}")
            return total_distance, area_1, area_2, area_3

        # Filter the coordinates based on the fill_y condition
        filtered_indices = np.where(y_additional <= fill_y)[0]
        x_filter = x_additional[filtered_indices]
        y_filter = y_additional[filtered_indices]

        length, area_1, area_2, area_3 = calculate_total_distance(x_filter, y_filter)
        v = (1 / n) * ((area_3 / length) ** (2 / 3)) * ((s / 1000) ** (1 / 2))
        q = area_3 * v
        
        with col3:
            col_1, col_2 = st.columns(spec=[0.50, 0.50], gap="small")
            with col_1:
                st.write(f"""> Wetted Area  
                        **:green[{area_3:.2f}]** m²""")
            with col_2:
                st.write(f"""> Velocity    
                        **:green[{v:.2f}]** m/Sec""")
            with col_1:
                st.write(f"""> Wetted Perimeter    
                        **:green[{length:.2f}]** m""")
            with col_2:
                st.write(f"""> Discharge  
                        **:green[{q:.2f}]** m³/Sec""")
    elif st.session_state.inputsentered:
        col2.error(":warning: Please Increase :arrow_up: Depth of Water Column field above :zero: for computations to run.")
    elif not st.session_state.inputsentry:
        col2.info(
            """ :keyboard: Please click on **:green[ENTER INPUTS]** button to proceed further. :dizzy:  
            \n  :snowman: The Cross-Sectional data table is freezed now.     
            \n  :exclamation: If you want to edit cross-section data table again, click on **:green[REFRESH]** button to go back to edit mode. :pencil: """
        )
        col2.error(""" :white_check_mark: The Cross-Sectional plot gives fairly accurate representation in most of the cases.   
                   \n  🚨 But in some cases (Refer Limitations page) the plot gives inaccurate representation of the data.  
                   \n  :thought_balloon: This can be resolved by adding more control points. If the issue persists please notify me (Refer Contact Page).""")
    else:
        col2.info(
            """:keyboard: Please enter the above input parameters and then click on **:green[COMPUTE]** button for results. :computer: 
            \n  :warning: Make sure to increase the Depth of Water Column field above :zero: for computations to run"""
        )
        col2.success("""Refer this website for Mannings Coefficient  
                     [Click Here](https://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm)""")
