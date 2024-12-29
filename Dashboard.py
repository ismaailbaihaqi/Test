import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_data = pd.read_csv('day_preprocessed.csv')
hour_data = pd.read_csv('hour_preprocessed.csv')

# Streamlit app configuration
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

st.title("Bike Sharing Data Analysis")

# Sidebar for dataset selection
st.sidebar.header("Dataset Selection")
dataset_choice = st.sidebar.radio("Choose Dataset:", ("Daily Data", "Hourly Data"))

if dataset_choice == "Daily Data":
    data = day_data
    st.subheader("Daily Data Overview")
else:
    data = hour_data
    st.subheader("Hourly Data Overview")

# Display data preview
st.write(data.head())

# Filter options
st.sidebar.header("Filters")
season_filter = st.sidebar.multiselect(
    "Filter by Season:",
    options=data["season"].unique(),
    default=data["season"].unique()
)
data_filtered = data[data["season"].isin(season_filter)]

# Plot selection
st.sidebar.header("Visualization")
plot_choice = st.sidebar.selectbox(
    "Choose a Plot:",
    ("Total Rentals by Day", "Rentals Distribution by Weather", "Trend Over Time", "Hourly Rental Patterns", "Daily Rentals by Weekday", "Average Rentals by Season", "Average Duration: Weekday vs Weekend")
)

if plot_choice == "Total Rentals by Day":
    fig = px.bar(
        data_filtered,
        x="dteday",
        y="cnt",
        title="Total Rentals by Day",
        labels={"dteday": "Date", "cnt": "Total Rentals"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_choice == "Rentals Distribution by Weather":
    fig = px.box(
        data_filtered,
        x="weathersit",
        y="cnt",
        title="Rentals Distribution by Weather",
        labels={"weathersit": "Weather Condition", "cnt": "Total Rentals"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_choice == "Trend Over Time":
    fig = px.line(
        data_filtered,
        x="dteday",
        y="cnt",
        title="Trend Over Time",
        labels={"dteday": "Date", "cnt": "Total Rentals"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif plot_choice == "Hourly Rental Patterns":
    if "hr" in data_filtered.columns:
        # Calculate average rentals by hour
        average_rentals_by_hour = data_filtered.groupby('hr')['cnt'].mean()

        # Create plot using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(average_rentals_by_hour.index, average_rentals_by_hour.values, marker='o', linestyle='-', color='b')
        ax.set_title('Pola Jumlah Penyewaan Sepeda Berdasarkan Jam dalam Sehari', fontsize=14)
        ax.set_xlabel('Jam', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)
        ax.set_xticks(range(0, 24))  # Display all hours from 0 to 23
        ax.grid(alpha=0.3)
        # Render the plot
        st.pyplot(fig)

elif plot_choice == "Daily Rentals by Weekday":
    # Mapping angka 0-6 ke nama hari
    day_name = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    data_filtered['weekday_name'] = data_filtered['weekday'].map(day_name)

    # Visualisasi menggunakan Seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=data_filtered['weekday_name'], y=data_filtered['cnt'], ax=ax)
    ax.set_xlabel('Weekday', fontsize=12)
    ax.set_ylabel('Number of Bike Rentals', fontsize=12)
    ax.set_title('Daily Bike Rentals by Weekday', fontsize=14)
    st.pyplot(fig)

elif plot_choice == "Average Rentals by Season":
    # Mapping angka 1-4 ke label musim
    season_labels = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    data_filtered['season_label'] = data_filtered['season'].map(season_labels)

    # Agregasi jumlah penyewaan berdasarkan musim
    seasonal_data = data_filtered.groupby('season_label')['cnt'].mean().reset_index()

    # Visualisasi pola musiman
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season_label', y='cnt', data=seasonal_data, palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda per Musim', fontsize=14)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Jumlah Penyewaan Rata-rata', fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

elif plot_choice == "Average Duration: Weekday vs Weekend":
    # Menambahkan label hari kerja/akhir pekan
    data_filtered['day_type'] = data_filtered['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Akhir Pekan')

    # Agregasi durasi penyewaan rata-rata per tipe hari
    data_filtered['avg_duration'] = data_filtered['cnt'] / (data_filtered['casual'] + data_filtered['registered'])
    day_type_data = data_filtered.groupby('day_type')['avg_duration'].mean().reset_index()

    # Visualisasi durasi penyewaan rata-rata
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='day_type', y='avg_duration', data=day_type_data, palette='viridis', ax=ax)
    ax.set_title('Durasi Penyewaan Rata-rata: Hari Kerja vs Akhir Pekan', fontsize=14)
    ax.set_xlabel('Tipe Hari', fontsize=12)
    ax.set_ylabel('Durasi Penyewaan Rata-rata (jam)', fontsize=12)
    st.pyplot(fig)


# Summary statistics
st.subheader("Summary Statistics")
st.write(data_filtered.describe())
