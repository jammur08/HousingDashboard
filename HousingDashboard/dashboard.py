


# Import the libraries needed for the dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the page title and layout
st.set_page_config(
    page_title="Irish Housing Market Explorer"
)

# Display the main title and description
st.title("Irish Housing Market Explorer")
st.write("Explore housing data and compare different areas of Ireland.")

# Add a divider below the heading
st.divider()

# Automatically read the CSV file
df = pd.read_csv("housing_data.csv")

# SECTION 1: DATA PREVIEW

st.subheader("Data Preview")

# Display the first five rows of the dataset
st.dataframe(df.head(), use_container_width=True)

# Display the number of rows and columns
st.write("Number of rows:", df.shape[0])
st.write("Number of columns:", df.shape[1])

st.divider()

# Find the columns that contain numbers
numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

# SECTION 2: SUMMARY STATISTICS

st.subheader("Summary Statistics")

# Check whether the dataset contains numeric columns
if len(numeric_columns) > 0:

    # Allow the user to select a column
    selected_column = st.selectbox(
        "Choose a column for the statistics",
        numeric_columns
    )

    # Remove empty values from the selected column
    values = df[selected_column].dropna()

    # Calculate and display statistics if values exist
    if len(values) > 0:

        # Display the mean, median and mode in three columns
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Mean",
            round(values.mean(), 2)
        )

        col2.metric(
            "Median",
            round(values.median(), 2)
        )

        # The mode is the most frequently occurring value
        mode_values = values.mode()

        if len(mode_values) > 0:
            col3.metric("Mode", str(mode_values.iloc[0]))
        else:
            col3.metric("Mode", "No mode")

    else:
        st.info("There are no values in this column.")

else:
    st.warning("No numeric columns were found.")

st.divider()

# SECTION 3: FULL DATA SUMMARY

st.subheader("Full Data Summary")

# Display statistics for all numeric columns
if len(numeric_columns) > 0:
    st.dataframe(
        df.describe(),
        use_container_width=True
    )
else:
    st.info("No numeric data is available for a summary.")

st.divider()

# SECTION 4: GENERATE A CHART

st.subheader("Generate a Chart")

# Allow the user to choose the X-axis
x_column = st.selectbox(
    "Choose the X-axis",
    df.columns.tolist()
)

# Only display the chart options if numeric columns exist
if len(numeric_columns) > 0:

    # Allow the user to choose the Y-axis
    y_column = st.selectbox(
        "Choose the Y-axis",
        numeric_columns
    )

    # Generate the chart when the button is clicked
    if st.button("Generate Chart"):

        # Select the two chosen columns and remove empty rows
        chart_data = df[[x_column, y_column]].dropna()

        # Check that there is data to display
        if len(chart_data) > 0:

            # Set the X-axis column as the chart index
            chart_data = chart_data.set_index(x_column)

            # Display the line chart
            st.line_chart(chart_data[y_column])

            # Explain what the chart displays
            st.caption(
                "Showing " + y_column +
                " against " + x_column + "."
            )

        else:
            st.warning("There is no data available for this chart.")

else:
    st.warning("A chart cannot be created without numeric columns.")
