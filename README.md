# Earthquake & Volcano Risk Dashboard

## Overview
This project is a real-time Earthquake and Volcano Risk Dashboard built with Python and Streamlit. It fetches live earthquake data from the USGS public API and volcano data from an open dataset to provide key insights, visualizations, and risk alerts.
A downloadable PDF report is generated using ReportLab, allowing for full Unicode support (including arrows and special characters) without the need to manage external font files.

## Features
- Fetches and displays recent earthquakes (last 1 hour) with magnitude > 2.5
- Loads volcano locations and details from an open CSV dataset
- Interactive KPIs for earthquake counts, average magnitude, max depth, and volcano count
- Alerts based on proximity of recent earthquakes to volcanoes (within 100 km)
- Time series plots and heatmaps of earthquake magnitudes
- Interactive volcano location map with hover details
- PDF report generation using ReportLab (Unicode safe, no external fonts needed)
- Fully open-source and uses only free public data and Python libraries

## Tech Stack
| Component | Technology / Library |
| -------- | -------- |
| Frontend UI |	Streamlit |
| Data Fetching |	Python requests + pandas |
| Visualization	| plotly.express |
| PDF Generation | ReportLab |
| Data Sources | USGS Earthquake API, Open Volcano Dataset CSV |

## Installation
1. Clone the repository:
`git clone https://github.com/yourusername/earthquake-volcano-dashboard.git
cd earthquake-volcano-dashboard`

2. Create and activate a Python environment (recommended):
`conda create -n eq_volcano python=3.9 -y
conda activate eq_volcano`
or
`python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows PowerShell`

3. Install dependencies:
`pip install -r requirements.txt`

## Usage
Run the Streamlit app:
`streamlit run app.py`
Open http://localhost:8501 in your browser to access the dashboard.

## PDF Report Generation
The PDF report is generated using ReportLab, which supports Unicode characters such as arrows (→) without requiring manual font file management.
### How it works
- Generates a multi-section report including KPIs and risk alerts.
- Uses built-in Helvetica font, which supports common Unicode characters.
- Exports the report as an in-memory byte stream for download in Streamlit.

## File Structure
```bash
earthquake-volcano-dashboard/
│
├── app.py                 # Main Streamlit app
├── data_fetch.py          # Functions to fetch earthquakes and volcanoes data
├── report_generator.py    # PDF generation using ReportLab
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Dependencies
- streamlit
- pandas
- requests
- plotly
- reportlab
You can install all at once via:
`pip install streamlit pandas requests plotly reportlab`

## Notes
- Volcano data is sourced from a static CSV file hosted on GitHub.
- Earthquake data refreshes hourly (configurable).
- Proximity alert radius is currently set to 100 km but can be adjusted.
- The app uses Plotly’s new density_map (MapLibre-based) for heatmaps to avoid Mapbox tokens.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.
