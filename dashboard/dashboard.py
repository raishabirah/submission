import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
current_directory = os.getcwd()
day_path = os.path.join(current_directory, "day.csv")
hour_path = os.path.join(current_directory, "hour.csv")

df_day = pd.read_csv(day_path)
df_hour = pd.read_csv(hour_path)

# Sidebar
st.sidebar.title("Proyek Analisis Data: Bike Sharing Dataset")
selected_analysis = st.sidebar.selectbox("Pilih Visualisasi", ["Dataset", "EDA", "Visualization & Explanatory Analysis"])

# Data yang Digunakan
if selected_analysis == "Dataset":
    st.subheader("Dataset day:")
    st.write(df_day)
    
    st.subheader("Dataset hour:")
    st.write(df_hour)

# EDA
elif selected_analysis == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    # Korelasi variabel numerik
    numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    correlation_matrix = df_day[numeric_cols].corr()
    fig_corr = px.imshow(correlation_matrix)
    fig_corr.update_layout(title="Korelasi antara Variabel Numerik")
    st.plotly_chart(fig_corr)

    # Distribusi variabel numerik
    st.subheader("Distribusi Variabel Numerik")
    for col in numeric_cols:
        fig_hist = px.histogram(df_day, x=col, title=f'Distribusi {col}')
        st.plotly_chart(fig_hist)

    # Distribusi variabel categorical
    st.subheader("Distribusi Variabel Kategorikal")
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        df_bar = df_day[col].astype(str).value_counts().reset_index()
        df_bar.columns = ['index', col]  # Reset the column names
        fig_bar = px.bar(df_bar, x='index', y=col, title=f'Distribusi {col}')
        st.plotly_chart(fig_bar)

# Visualization & Explanatory Analysis
elif selected_analysis == "Visualization & Explanatory Analysis":
    st.header("Visualization & Explanatory Analysis")

    # Visualisasi Kondisi Cuaca
    fig_weathersit = px.bar(df_day.groupby("weathersit")["cnt"].mean().reset_index(), 
                            x="weathersit", y="cnt",
                            title="Rata-rata Peminjaman Sepeda berdasarkan Kondisi Cuaca",
                            labels={"weathersit": "Kondisi Cuaca", "cnt": "Rata-rata Peminjaman"})
    st.plotly_chart(fig_weathersit)

    st.markdown('Weather:')
    st.markdown('1: Clear, Few clouds, Partly cloudy, Partly cloudy')
    st.markdown('2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist')
    st.markdown('3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds')
    st.markdown('4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog')

    # Pola Harian Peminjaman Sepeda
    fig_hour = px.bar(df_hour, x="hr", y="cnt", color=None, 
                      title="Perbandingan Peminjaman Sepeda Harian",
                      labels={"hr": "Jam", "cnt": "Jumlah Peminjaman", "workingday": "Hari Kerja"},
                      category_orders={"workingday": [0, 1]},
                      facet_col="workingday",
                      height=400)
    fig_hour.update_xaxes(tickvals=list(range(24)))
    fig_hour.for_each_annotation(lambda a: a.update(text='Libur' if '0' in a.text else 'Hari Kerja'))
    st.plotly_chart(fig_hour)

    # Pola Peminjaman Sepeda per Tahun
    df_day['year'] = pd.to_datetime(df_day['dteday']).dt.year

    fig_yearly_pattern = px.bar(df_day, x="mnth", y="cnt", color="year",
                                title="Perbandingan Peminjaman Sepeda Tahun 2011 dan 2012",
                                labels={"mnth": "Bulan", "cnt": "Jumlah Peminjaman", "year": "Tahun"},
                                category_orders={"mnth": list(range(1, 13))},
                                height=400)

    fig_yearly_pattern.update_layout(barmode='group')
    st.plotly_chart(fig_yearly_pattern)
