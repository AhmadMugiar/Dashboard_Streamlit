import streamlit as st
from data import load_data, filter_data, show_data, select_year, select_location, kolom, pie_chart, bar_chart1, bar_chart2, map_chart

def judul():
    st.title("Dashboard COVID-19")
    st.write("Selamat Datang di Dashboard interaktif untuk menganalisis data Covid di Indonesia")
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])
if menu == "Home":
    judul()
    df = load_data()
    year = select_year()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    kolom(df_filtered)
    pie_chart(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
elif menu == "Halaman Data":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 Ahmad Mugiar Sujana. All rights reserved.</div>", unsafe_allow_html=True)
