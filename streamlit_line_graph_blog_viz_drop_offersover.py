import streamlit as st
import pandas as pd
import altair as alt

# Load the CSV file
csv_file = 'data/blog_viz.csv'
data = pd.read_csv(csv_file)

# Rename columns for easier reference
data.rename(columns={
    "address.outcode": "Postcode",
    "year_sale": "Year",
    "sample_listed_sold": "Sample",
    "min_listed_sold_percentage": "Minimum % Over Listing Price",
    "lower_quartile_listed_sold_percentage": "Lower Quartile % Over Listing Price",
    "median_listed_sold_percentage": "Median % Over Listing Price",
    "mean_listed_sold_percentage": "Average % Over Listing Price",
    "upper_quartile_listed_sold_percentage": "Upper Quartile % Over Listing Price",
    "max_listed_sold_percentage": "Maximum % Over Listing Price"
}, inplace=True)

# Convert "Year" column to datetime type
data["Year"] = pd.to_datetime(data["Year"], format="%Y")

# Round the specified columns to two decimal places
columns_to_round = [
    "Minimum % Over Listing Price",
    "Lower Quartile % Over Listing Price",
    "Median % Over Listing Price",
    "Average % Over Listing Price",
    "Upper Quartile % Over Listing Price",
    "Maximum % Over Listing Price"
]

data[columns_to_round] = data[columns_to_round].round(2)

# Get sorted unique postcodes
sorted_postcodes = sorted(data["Postcode"].unique())

# Sidebar
st.sidebar.title("Filter Options")

# Automatically select all postcodes by default
selected_postcodes = st.sidebar.multiselect(
    "Select Postcodes", sorted_postcodes, default=sorted_postcodes)

# Always include the "Average % Over Listing Price" in selected_values
selected_values = ['Average % Over Listing Price']

# Filter the data based on selected options
filtered_data = data[data["Postcode"].isin(selected_postcodes)]
filtered_data = filtered_data[["Year", "Postcode", "Sample"] + selected_values]

# Calculate the maximum and minimum y-axis values based on selected values
# Adjust for a better visualization
max_y = filtered_data[selected_values].max().max() * 1.1
# Adjust scale for negative values
min_y = filtered_data[selected_values].min().min() * 1.1

# Line Chart with Points
st.title("% Over Listing Price")
if len(selected_postcodes) > 0:
    base = alt.Chart(filtered_data).encode(
        x="Year:T",  # Specify the format here to display only years
        y=alt.Y(alt.repeat("row"), type="quantitative",
                scale=alt.Scale(domain=(min_y, max_y))),
        color="Postcode:N",
        tooltip=["Postcode", alt.Tooltip(
            "year(Year):O", title="Year"), "Sample"] + selected_values
    ).properties(
        width=1000,
        height=600
    )

    line = base.mark_line()

    points = base.mark_circle(size=50)

    chart = alt.layer(line, points).repeat(
        row=selected_values
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

else:
    st.write("Please select at least one postcode to plot.")
