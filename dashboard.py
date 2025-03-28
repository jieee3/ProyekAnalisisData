import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
all_data = pd.read_csv("all_data.csv")

# Konversi tanggal ke format datetime
all_data["dteday"] = pd.to_datetime(all_data["dteday"])


# Sidebar untuk filter rentang tanggal
min_date = all_data["dteday"].min()
max_date = all_data["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataset berdasarkan rentang tanggal
filtered_data = all_data[(all_data["dteday"] >= pd.to_datetime(start_date)) & 
                         (all_data["dteday"] <= pd.to_datetime(end_date))]

# **Menghitung total peminjaman sepeda per hari dalam seminggu**
if "weekday_day" in filtered_data.columns and "cnt_day" in filtered_data.columns:
    daily_bike_rentals = filtered_data.groupby("weekday_day")["cnt_day"].sum()
elif "weekday_hour" in filtered_data.columns and "cnt_hour" in filtered_data.columns:
    daily_bike_rentals = filtered_data.groupby("weekday_hour")["cnt_hour"].sum()
else:
    st.error("Kolom weekday dan cnt tidak ditemukan!")


# **Menghitung total peminjaman sepeda per jam dalam sehari**
if "hr" in filtered_data.columns and "cnt_hour" in filtered_data.columns:
    hour_bike_rentals = filtered_data.groupby("hr")["cnt_hour"].sum()
else:
    st.error("Kolom hr dan cnt_hour tidak ditemukan!")

# Label untuk hari dalam seminggu
weekday_labels = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Menampilkan judul dashboard
st.title("Dashboard Peminjaman Sepeda 🚴‍♂️")

# **Visualisasi Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu**
st.subheader("Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=daily_bike_rentals.index, y=daily_bike_rentals.values, palette="Purples", ax=ax)
ax.set_title("Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_xticks(range(7))
ax.set_xticklabels(weekday_labels, rotation=45)
st.pyplot(fig)

# **Fitur Interaktif: Slider untuk Memfilter Rentang Jam**
st.sidebar.subheader("Filter Rentang Jam")
min_hour, max_hour = st.sidebar.slider("Pilih Rentang Jam", 0, 23, (0, 23))

# Filter data berdasarkan jam yang dipilih
filtered_hour_bike_rentals = hour_bike_rentals.loc[min_hour:max_hour]

# **Visualisasi Total Peminjaman Sepeda Berdasarkan Jam dalam Sehari**
st.subheader(f"Total Peminjaman Sepeda Berdasarkan Jam dalam sehari ({min_hour}:00 - {max_hour}:00)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=filtered_hour_bike_rentals.index, y=filtered_hour_bike_rentals.values, palette="Purples", ax=ax)
ax.set_title(f"Total Peminjaman Sepeda Berdasarkan Jam dalam sehari")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_ylim(0, hour_bike_rentals.max() * 1.1)  # Menyesuaikan skala sumbu Y
st.pyplot(fig)

st.caption("by Rosievi hijrih juniar.2025")
