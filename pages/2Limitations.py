import streamlit as st

st.set_page_config(
    page_title="SF Discharge Limitations",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("""**:violet[Need for this App]  :thought_balloon:**  
        Stream Cross-Sections are irregular in shape and highly dynamic in nature which makes manual calculation of **Wetted Area** and **Wetted Perimeter** with fluctuation of water depth a tedious task.  
        \n  This App is intended to Simplify this task by making use of Interpolation Techniques and Numerical Methods in Python and then calculate **Velocity** and **Discharge** of the stream for different input parameters.  
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


st.markdown("""
#### 🚨 Limitations and Assumptions

**These are the limitations and assumptions of this application and some are based on my perspective:**       

:star: It is assumed that stream bed is fixed for certain period to get started even though it is highly variable in nature. The bed keeps changing due to continuous cycle of deposition and transportation of sediment due to erosion.   

:star: The curve is fitted for the cross-sectional data using piece wise interpolation (cubic polynomial by default) and gives fairly accurate representation in most of the cases but rarely the curve may give inaccurate representation due to lack of data points or due to alteration from steep fall to gentle fall in elevations.    

:star: The Depth of the Water Column is from the deepest point and ideally the sensor measuring the water column depth needs to be positioned above the deepest point of cross-section but that may not be true in field for some streams.  

:star: Discharge computations are done using Mannings formula which gives good results but is highly sensitive to the coefficient value.  

:star: Mannings equation works better for man-made channels/canals due to fair estimate of coefficient rather than natural streams due to high variability of bed conditions as mentioned earlier that makes them difficult for estimating coefficient.    
""")