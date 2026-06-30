# Employee Performance Analysis

This is my internship project where I analyze employee data (salary, attendance,
performance, department, education, city) using Python and Streamlit.

The data cleaning and EDA part was first done in a Jupyter Notebook, and later
I converted it into this interactive Streamlit web app.

## Features

- **Home Page** – project intro, KPI cards, dataset snapshot
- **Dataset Page** – preview, shape, datatypes, summary statistics
- **Data Cleaning Page** – missing values, duplicate detection/removal, IQR-based outlier detection with boxplots
- **Visualizations Page** – histograms, boxplots, scatter plots, line chart, pie chart, bar charts, heatmap, bubble chart, regression trend, and more, all built with Plotly
- **Sidebar Filters** – filter by Department, City, Education Level, and Performance Category (applies to the whole app)
- **Insights Page** – auto-calculated KPIs like highest/lowest/average salary, best performing department, etc.
- **Download Page** – download the currently filtered data as CSV

## Project Structure

```
Employee-Performance-Analysis/
│
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── employee_dataset.csv
```

## How to Run Locally

1. Clone this repository
   ```
   git clone <your-repo-link>
   cd Employee-Performance-Analysis
   ```

2. (Optional) create a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install requirements
   ```
   pip install -r requirements.txt
   ```

4. Make sure your dataset is placed at `data/employee_dataset.csv`

5. Run the app
   ```
   streamlit run app.py
   ```

## Deployment on Streamlit Community Cloud

1. Push this whole project (including the `data/` folder with the CSV) to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New app"**, then select:
   - Repository: your repo
   - Branch: `main`
   - Main file path: `app.py`
4. Click **Deploy**. Streamlit Cloud will install everything from `requirements.txt` automatically.
5. Once deployed, you'll get a public link you can share (e.g. in your internship report).

## Tech Used

- Python
- Pandas / NumPy
- Streamlit
- Plotly Express

## Author

Built as part of my internship project on Employee Performance Analysis.
