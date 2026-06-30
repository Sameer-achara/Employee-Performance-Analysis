

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os


st.set_page_config(
    page_title="Employee Performance Analysis",
    layout="wide"
)


MAIN_COLOR = "#4C72B0"



@st.cache_data
def load_data():
    

    BASE_DIR= os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "employee_dataset_powerbi.csv")

    df = pd.read_csv(DATA_PATH)

    # the attendance column has a % sign in it, need to clean that
    if "Attendance_Percentage" in df.columns:
        df["Attendance_Percentage"] = (
            df["Attendance_Percentage"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.strip()
        )

        df["Attendance_Percentage"] = pd.to_numeric(
            df["Attendance_Percentage"],
            errors="coerce"
        )


raw_df = load_data()



st.sidebar.title("Employee Performance Analysis")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Dataset", "Data Cleaning", "Visualizations", "Insights", "Download"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")


dept_options = sorted(raw_df["department"].dropna().unique())
city_options = sorted(raw_df["City"].dropna().unique())
edu_options = sorted(raw_df["education_level"].dropna().unique())
perf_options = sorted(raw_df["performance_category"].dropna().unique())

selected_dept = st.sidebar.multiselect("Department", dept_options, default=dept_options)
selected_city = st.sidebar.multiselect("City", city_options, default=city_options)
selected_edu = st.sidebar.multiselect("Education Level", edu_options, default=edu_options)
selected_perf = st.sidebar.multiselect("Performance Category", perf_options, default=perf_options)


df = raw_df[
    (raw_df["department"].isin(selected_dept)) &
    (raw_df["City"].isin(selected_city)) &
    (raw_df["education_level"].isin(selected_edu)) &
    (raw_df["performance_category"].isin(selected_perf))
]

if df.empty:
    st.warning("No data matches the selected filters. Please change filter options.")
    st.stop()



if page == "Home":
    st.title("Employee Performance Analysis Dashboard")
    st.write(
        """
        This project analyzes employee data to understand patterns in salary,
        attendance, and performance across departments, cities and education levels.
        It was originally done in a Jupyter Notebook (data cleaning + EDA) and is now
        converted into this interactive Streamlit app for my internship submission.
        """
    )

    st.subheader("Quick Overview (based on current filters)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", len(df))
    col2.metric("Average Salary", f"₹{df['Salary'].mean():,.0f}")
    col3.metric("Average Attendance", f"{df['Attendance_Percentage'].mean():.1f}%")
    col4.metric("Average Experience", f"{df['years_experience'].mean():.1f} yrs")

    st.markdown("---")
    st.subheader("Dataset Snapshot")
    st.dataframe(df.head(10))

    st.caption("Use the sidebar to filter the data and navigate between pages.")




elif page == "Dataset":
    st.title("Dataset Overview")

    st.subheader("Preview")
    st.dataframe(df.head(20))

    st.subheader("Shape of Data")
    st.write(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

    st.subheader("Column Data Types")
    dtype_df = pd.DataFrame(df.dtypes, columns=["Data Type"])
    st.dataframe(dtype_df)

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())



elif page == "Data Cleaning":
    st.title("Data Cleaning")

    st.subheader("Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing.index]  # keep all columns visible
    st.dataframe(missing.rename("Missing Count"))

    if missing.sum() == 0:
        st.success("No missing values found in the current data.")

    st.subheader("Duplicate Rows")
    dup_count = df.duplicated().sum()
    st.write(f"Total duplicate rows found: **{dup_count}**")

    if dup_count > 0:
        st.dataframe(df[df.duplicated()])
        if st.button("Remove Duplicate Rows"):
            df = df.drop_duplicates()
            st.success(f"Duplicates removed. New shape: {df.shape}")
    else:
        st.success("No duplicate rows found.")

    st.markdown("---")
    st.subheader("Outlier Detection (IQR Method)")

    numeric_cols = ["age", "years_experience", "performance_score"]
    chosen_col = st.selectbox("Choose a column to check for outliers", numeric_cols)

    Q1 = df[chosen_col].quantile(0.25)
    Q3 = df[chosen_col].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[(df[chosen_col] < lower_limit) | (df[chosen_col] > upper_limit)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Lower Limit", round(lower_limit, 2))
    col2.metric("Upper Limit", round(upper_limit, 2))
    col3.metric("Outliers Found", len(outliers))

    fig = px.box(df, x=chosen_col, color_discrete_sequence=[MAIN_COLOR],
                 title=f"Boxplot of {chosen_col}")
    st.plotly_chart(fig, use_container_width=True)



elif page == "Visualizations":
    st.title("Visualizations")
    st.write("All charts below update automatically based on the sidebar filters.")

    # ---- Histograms ----
    st.subheader("Distributions")
    hist_col = st.selectbox(
        "Select a column for histogram",
        ["age", "years_experience", "Salary", "Attendance_Percentage"]
    )
    fig = px.histogram(df, x=hist_col, nbins=20, color_discrete_sequence=[MAIN_COLOR],
                        marginal="box", title=f"Distribution of {hist_col}")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Boxplot ----
    st.subheader("Boxplot")
    box_col = st.selectbox("Select column for boxplot", ["age", "Salary", "performance_score"])
    fig = px.box(df, y=box_col, color_discrete_sequence=[MAIN_COLOR], title=f"Boxplot - {box_col}")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Scatter Plot ----
    st.subheader("Scatter Plot")
    c1, c2 = st.columns(2)
    x_axis = c1.selectbox("X-axis", ["age", "years_experience", "Attendance_Percentage"], key="scatter_x")
    y_axis = c2.selectbox("Y-axis", ["Salary", "performance_score"], key="scatter_y")
    fig = px.scatter(df, x=x_axis, y=y_axis, color="department",
                      title=f"{x_axis} vs {y_axis}")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Line Chart (Performance trend by experience) ----
    st.subheader("Performance Trend by Experience")
    exp_perf = df.groupby("years_experience")["performance_score"].mean().reset_index()
    fig = px.line(exp_perf, x="years_experience", y="performance_score",
                   markers=True, color_discrete_sequence=[MAIN_COLOR],
                   title="Average Performance Score by Years of Experience")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Pie Chart ----
    st.subheader("Pie Chart")
    pie_col = st.selectbox("Select category for pie chart",
                            ["department", "education_level", "performance_category", "City"])
    pie_data = df[pie_col].value_counts().reset_index()
    pie_data.columns = [pie_col, "count"]
    fig = px.pie(pie_data, names=pie_col, values="count", title=f"Share by {pie_col}")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Bar Chart - Department Analysis ----
    st.subheader("Department Analysis")
    dept_salary = df.groupby("department")["Salary"].mean().reset_index()
    fig = px.bar(dept_salary, x="department", y="Salary", color_discrete_sequence=[MAIN_COLOR],
                 title="Average Salary by Department")
    st.plotly_chart(fig, use_container_width=True)

    dept_attendance = df.groupby("department")["Attendance_Percentage"].mean().reset_index()
    fig = px.bar(dept_attendance, x="department", y="Attendance_Percentage",
                 color_discrete_sequence=[MAIN_COLOR], title="Average Attendance by Department")
    st.plotly_chart(fig, use_container_width=True)

    # ---- City Analysis ----
    st.subheader("City Analysis")
    city_salary = df.groupby("City")["Salary"].mean().reset_index().sort_values("Salary", ascending=False)
    fig = px.bar(city_salary, x="City", y="Salary", color_discrete_sequence=[MAIN_COLOR],
                 title="Average Salary by City")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Attendance Analysis ----
    st.subheader("Attendance vs Performance")
    fig = px.scatter(df, x="Attendance_Percentage", y="performance_score", color="department",
                      title="Attendance Percentage vs Performance Score")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Salary Analysis (by education) ----
    st.subheader("Salary Analysis by Education Level")
    fig = px.box(df, x="education_level", y="Salary", color="education_level",
                 title="Salary Spread by Education Level")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Bubble Chart ----
    st.subheader("Bubble Chart - Age vs Salary (size = Experience)")
    fig = px.scatter(df, x="age", y="Salary", size="years_experience", color="department",
                      size_max=40, title="Age vs Salary (Bubble size = Years of Experience)")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Regression Trend ----
    st.subheader("Regression Trend - Experience vs Salary")
    fig = px.scatter(df, x="years_experience", y="Salary", trendline="ols",
                      color_discrete_sequence=[MAIN_COLOR],
                      title="Experience vs Salary with Trend Line")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Heatmap ----
    st.subheader("Correlation Heatmap")
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                     title="Correlation Between Numerical Columns")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Performance Analysis ----
    st.subheader("Performance Category Count")
    perf_count = df["performance_category"].value_counts().reset_index()
    perf_count.columns = ["performance_category", "count"]
    fig = px.bar(perf_count, x="performance_category", y="count",
                 color_discrete_sequence=[MAIN_COLOR], title="Number of Employees per Performance Category")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Top 10 Employees by Salary ----
    st.subheader("Top 10 Employees by Salary")
    top10_salary = df.nlargest(10, "Salary")
    fig = px.bar(top10_salary, x="Salary", y=top10_salary.index.astype(str),
                 orientation="h", color_discrete_sequence=[MAIN_COLOR],
                 title="Top 10 Highest Paid Employees")
    fig.update_layout(yaxis_title="Employee Index")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Top 10 Performers ----
    st.subheader("Top 10 Performers (Score + Attendance)")
    top10_perf = df.nlargest(10, ["performance_score", "Attendance_Percentage"])
    fig = px.bar(top10_perf, x="Attendance_Percentage", y=top10_perf.index.astype(str),
                 orientation="h", color_discrete_sequence=[MAIN_COLOR],
                 title="Top 10 Performers by Score & Attendance")
    fig.update_layout(yaxis_title="Employee Index")
    st.plotly_chart(fig, use_container_width=True)



elif page == "Insights":
    st.title("Key Insights")
    st.write("These insights are calculated automatically based on the filtered data.")

    dept_perf = df.groupby("department")["performance_score"].mean()
    best_perf_dept = dept_perf.idxmax()

    dept_sal = df.groupby("department")["Salary"].mean()
    best_salary_dept = dept_sal.idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Salary", f"₹{df['Salary'].max():,.0f}")
    col2.metric("Lowest Salary", f"₹{df['Salary'].min():,.0f}")
    col3.metric("Average Salary", f"₹{df['Salary'].mean():,.0f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Average Attendance", f"{df['Attendance_Percentage'].mean():.1f}%")
    col5.metric("Average Experience", f"{df['years_experience'].mean():.1f} yrs")
    col6.metric("Total Employees", len(df))

    col7, col8 = st.columns(2)
    col7.metric("Best Performing Department", best_perf_dept)
    col8.metric("Highest Avg Salary Department", best_salary_dept)

    st.markdown("---")
    st.subheader("Department-wise Summary Table")
    summary = df.groupby("department").agg(
        avg_salary=("Salary", "mean"),
        avg_performance=("performance_score", "mean"),
        avg_attendance=("Attendance_Percentage", "mean"),
        total_employees=("department", "count")
    ).round(2)
    st.dataframe(summary)




elif page == "Download":
    st.title("Download Filtered Data")
    st.write("You can download the dataset based on the filters currently applied from the sidebar.")

    st.dataframe(df.head(20))

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_employee_data.csv",
        mime="text/csv"
    )
