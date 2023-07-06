import streamlit as st

st.set_page_config(
    page_title="SF Discharge Contact",
    page_icon=":email:",
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


st.info("""Please contact me for any Queries, Suggestions or to Report Bugs in the Application      
        :construction_worker: **Name & Designation**       
        Ashok Guntu    
        Assistant Hydrologist  
        :office: **Office**    
        District Data Center  
        Ground Water and Water Audit Department  
        NTR District  
        :email: **Email**    
        ashokgwork@gmail.com 
""")