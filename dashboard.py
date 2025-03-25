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
if "weekday" in filtered_data.columns and "cnt" in filtered_data.columns:
    daily_bike_rentals = filtered_data.groupby("weekday")["cnt"].sum()
else:
    st.error("Kolom weekday dan cnt tidak ditemukan!")

# **Menghitung total peminjaman sepeda per jam dalam sehari**
if "hr" in filtered_data.columns and "cnt" in filtered_data.columns:
    hour_bike_rentals = filtered_data.groupby("hr")["cnt"].sum()
else:
    st.error("Kolom hr dan cnt tidak ditemukan!")

# Fungsi untuk menghitung total peminjaman berdasarkan kategori tertentu
def calculate_rentals(df):
    return {
        "holiday": df.groupby("holiday")["cnt"].sum(),
        "weekday": df.groupby("weekday")["cnt"].sum(),
        "workingday": df.groupby("workingday")["cnt"].sum(),
        "season": df.groupby("season")["cnt"].sum(),
    }

rental_data = calculate_rentals(filtered_data)

# Label untuk hari dalam seminggu
weekday_labels = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Menampilkan judul dashboard
st.title("Dashboard Peminjaman Sepeda 🚴‍♂️")

# **Visualisasi Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu**
st.subheader("Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=weekday_labels, y=daily_bike_rentals.values, palette="Purples", ax=ax)
ax.set_title("Total Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_xticklabels(weekday_labels, rotation=45)

# **Mencegah batang data menyentuh batas atas**
ax.set_ylim(0, daily_bike_rentals.max() * 1.1)

# Menghapus titik/koma pada angka di sumbu Y
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))

st.pyplot(fig)

# **Fitur Interaktif: Slider untuk Memfilter Rentang Jam**
st.sidebar.subheader("Filter Rentang Jam")
min_hour, max_hour = st.sidebar.slider("Pilih Rentang Jam", 0, 23, (0, 23))

# Filter data berdasarkan jam yang dipilih
filtered_hour_bike_rentals = hour_bike_rentals.loc[min_hour:max_hour]

# **Visualisasi Total Peminjaman Sepeda Berdasarkan Jam dalam Sehari**
st.subheader(f"Total Peminjaman Sepeda Berdasarkan Jam ({min_hour}:00 - {max_hour}:00) dalam sehari")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=filtered_hour_bike_rentals.index, y=filtered_hour_bike_rentals.values, palette="Purples", ax=ax)
ax.set_title(f"Total Peminjaman Sepeda Berdasarkan Jam ({min_hour}:00 - {max_hour}:00)")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Total Peminjaman Sepeda")

# **Mencegah batang data menyentuh batas atas**
ax.set_ylim(0, filtered_hour_bike_rentals.max() * 1.1)

# Menghapus titik/koma pada angka di sumbu Y
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))

st.pyplot(fig)

st.caption("by Rosievi Hijrih Juniar, 2025")
