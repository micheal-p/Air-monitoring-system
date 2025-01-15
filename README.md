
### README.md

```markdown
# Air Quality Monitoring System

A web application that monitors air quality in Nigerian cities using real-time data from the OpenWeatherMap API. It provides detailed insights into various pollutants, calculates an AQI percentage score, and visualizes data with Streamlit, Matplotlib, and Seaborn. Data is stored in SQLite for historical analysis.

## Features

- Real-Time Data Fetching: Fetches air quality data from OpenWeatherMap API.
- Data Visualization: Visualizes pollutant levels using Matplotlib and Seaborn.
- Air Quality Index (AQI): Calculates and displays AQI percentage score.
- Historical Data Storage: Stores data in SQLite for future reference.
- Interactive UI: Provides an interactive user interface using Streamlit.

## Demo

![Air Quality Monitoring System Demo](demo.gif)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/air-quality-monitoring-system.git
    cd air-quality-monitoring-system
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask API:
    ```sh
    python air_quality_api.py
    ```

2. Launch the Streamlit application:
    ```sh
    streamlit run air_quality_ui.py
    ```

3. Open your browser and go to `http://localhost:8501` to interact with the application.

## Example

1. Enter the name of a Nigerian state in the input field.
2. Click on the "Search" button to fetch and display the air quality data.
3. View the AQI percentage score and pollutant levels in the interactive charts.

## Screenshots

### Input State
![Input State](images/input_state.png)

### Data Visualization
![Data Visualization](images/data_visualization.png)

## Project Structure


air-quality-monitoring-system/
├── air_quality_api.py      # Flask API to fetch and store air quality data
├── air_quality_ui.py       # Streamlit UI to display air quality data
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── images/                 # Folder containing screenshots and GIFs
``

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License

This project is licensed under the MIT License. Please look at the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenWeatherMap API](https://openweathermap.org/api) for providing air quality data.
- [Streamlit](https://www.streamlit.io/) for the interactive UI framework.
- [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/) for data visualization.

```


This README provides a comprehensive overview of your project, including installation instructions, usage examples, and visual demonstrations to enhance user understanding.
