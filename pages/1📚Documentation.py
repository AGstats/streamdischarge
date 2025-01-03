import streamlit as st

st.set_page_config(
    page_title="SF Discharge Documentation",
    page_icon="📚",
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


st.info('📚 This page explains the underlying logic and computations powering this application')

st.markdown("""
            The objective of this App is to save time and labour involved in calculating stream cross-sectional 
            properties thereby arriving velocity and discharge of a stream. 
            This App simplifies this task and gives reasonably accurate results in couple of minutes which otherwise takes hours to arrive manually.
            This App is designed to be self explanatory by giving suitable instructions in every step. So, please read those instructions atleast during your initial use.

            **:red[Problem Statement] :lock:**
            
            :star: Stream discharge calculation is an important aspect for assessment of water availability in the basin. Different methods can be adopted for calculating stream discharge. 
            
            :star: It can be measured every day in field by profiling the cross-section and using current meter for velocity. But this needs a dedicated guaging station which may not be feasible for every stream flow check point due to costs involved. 
            
            :star: In order to reduce the man power and infrastructure that is needed for dedicated stream guage stations, Sensors can be installed to assess depth of flow at a particular stream cross-section. But depth of flow is only first step in arriving stream discharge.
            
            :star: Stream cross-sectional properties of wetted area and wetted perimeter that vary with depth of water flow are required for calculation of stream discharge using Mannings equation. 
            
            :star: As you might have seen in the quick sidebar of this App, stream cross-sections are irregular in shape so calculating the wetted area and wetted perimeter of a dynamic cross-section at changing depths everytime manually is a cumbersome activity. 
            
            **:green[Solution] :key:**

            :star: This App is designed to simplify the problem we discussed earlier using curve fitting, interpolation and numerical methods in python. At first I contemplated to solve this problem using python in jupyter notebook only but then went on to create a web app so that more users will get benefitted.
            
            :star: This web app is designed using streamlit which is a popular python library for creating web apps using just python. Streamlit components render HTML, CSS and Javacript to the web page under the hood. So, I just used python code all the way in creating this web app. 
            
            :star: To make this transparent in showing how calculations are performed in the background so that users can proceed with much confidence, here are 5 important aspects of how this App works in the backend.

            :one: Fitting a curve to the control points which are the relative elevations across respective cross-sectional distances from bank. As the stream cross-section doesn't fit into any single curve equation, Piece wise interpolation is used in fitting curve to the control points using SciPy library. It's just like how smoothing in excel graphs work but this app defines the underlying smoothing algorithm that provides more options to fit the curve.

            :two: To improve accuracy we added more control points through interpolation using the curve we fitted earlier (Added one point for every centimeter). This curve is then clipped to the extent of water depth specified for further calculations.
            
            :three: The wetted area is calculated using Trapezoidal method. This App intentionally opted for trapezoidal method over simpsons as the wetted area can be discontinuous in some cases to which simpsons rule gives inaccurate results due to the nature of quadratic polynomial fitted between discontinuous sections. The accuracy advantage of using simpsons is negligible here as we generated control points for every centimeter earlier.
            
            :four: The wetted perimeter is calculated using simple Euclidean distance method between consecutive points. Non-conscutive points that may arise out of discontinuos sections of water are filtered out before calculating perimeter. 
            
            :five: Then finally calculation of Velocity and Discharge using Mannings formula is a straight forward approach using longitudinal slope and suitable Mannings coefficient in addition to the Wetted area and Wetted perimeter we calculated earlier.





""")
