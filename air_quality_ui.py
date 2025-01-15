import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

API_URL = 'http://127.0.0.1:5000/api/air-quality'

st.title('Air Quality Monitoring System')

# User input for state
state = st.text_input('Enter a Nigerian State:')

# Function to convert AQI to an exact percentage score using linear interpolation
def aqi_to_percentage(aqi):
    if aqi <= 50:
        return 100 - (aqi / 50) * 20  # Good
    elif aqi <= 100:
        return 80 - ((aqi - 50) / 50) * 20  # Moderate
    elif aqi <= 150:
        return 60 - ((aqi - 100) / 50) * 20  # Unhealthy for Sensitive Groups
    elif aqi <= 200:
        return 40 - ((aqi - 150) / 50) * 20  # Unhealthy
    elif aqi <= 300:
        return 20 - ((aqi - 200) / 100) * 20  # Very Unhealthy
    else:
        return max(0, 20 - ((aqi - 300) / 100) * 20)  # Hazardous

if st.button('Search'):
    if state:
        with st.spinner('Fetching air quality data...'):
            time.sleep(2)  # Simulate a delay for loading
            response = requests.get(f'{API_URL}?state={state}')
            if response.status_code == 200:
                data = response.json()
                
                # Display the data in a detailed format
                st.write("### Air Quality Data")
                df = pd.DataFrame([data])
                st.dataframe(df)

                # Calculate and display air quality as an exact percentage
                aqi = data['aqi']
                air_quality_percentage = aqi_to_percentage(aqi)
                st.metric('Air Quality Percentage', f"{air_quality_percentage:.2f}%")

                # Plotting the pollutant levels
                st.write("### Pollutant Levels")
                pollutant_data = {
                    "Pollutant": ["PM2.5", "PM10", "CO", "NO2", "O3", "SO2"],
                    "Concentration": [data["pm2_5"], data["pm10"], data["co"], data["no2"], data["o3"], data["so2"]]
                }
                pollutant_df = pd.DataFrame(pollutant_data)
                fig, ax = plt.subplots()
                sns.barplot(x="Pollutant", y="Concentration", data=pollutant_df, ax=ax)
                ax.set_title("Pollutant Concentration Levels")
                ax.set_ylabel("Concentration (µg/m³ or ppm)")
                ax.set_xlabel("Pollutant")
                st.pyplot(fig)
                
                # Explanation of the air quality percentage
                st.write(f"""
                    **Air Quality Percentage Explanation**:
                    - **100%**: Good air quality with AQI between 0-50.
                    - **80%**: Moderate air quality with AQI between 51-100.
                    - **60%**: Unhealthy for sensitive groups with AQI between 101-150.
                    - **40%**: Unhealthy air quality with AQI between 151-200.
                    - **20%**: Very unhealthy air quality with AQI between 201-300.
                    - **0%**: Hazardous air quality with AQI above 300. 
                """)
            elif response.status_code == 404:
                st.error('State not found. Please enter a valid Nigerian state.')
            else:
                st.error('Error fetching data. Please try again later.')
    else:
        st.warning('Please enter a state.')