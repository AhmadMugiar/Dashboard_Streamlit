import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, location=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location and location != "Semua Provinsi":
        df= df[df['Location'].isin(location)]    
    return df

def select_year():
    return st.sidebar.selectbox(
        "📅 Pilih Tahun",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "📊 Semua Tahun" if x is None else x
    )
def select_location(df):
    locations = ["Semua Provinsi"] + sorted (df['Location'].unique())
    return st.sidebar.multiselect("Pilih Provinsi",
        options=locations)
    
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("📋 Data COVID-19 Indonesia")
    st.dataframe(df_selected.head(10))
    st.header("Statistika Desktiftip Dataset")
    st.write(df_selected.describe())

# Total Kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_kasus['Total Cases'].sum()
# Total Death
def total_death(df):
    total_kematian = df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_kematian['Total Deaths'].sum()
# Total Sembuh
def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location',as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

# Kolom 1
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🦠 Total Kasus", value=f"{kasus:,.0f}".replace(",", "."),border=True)
    col2.metric(label="💀 Total Kematian", value=f"{kematian:,.0f}".replace(",", "."),border=True)
    col3.metric(label="💚 Total Sembuh", value=f"{sembuh:,.0f}".replace(",", "."),border=True)

def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')
    fig = px.bar(
        top5,
        x='Location', y='Total Deaths',
        color = 'Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan kematian tertinggi',
        labels={'Total Deaths':'Total Kematian','Location':'Provinsi'}
    )
    fig.update_layout(xaxis_title= 'Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'New Recovered')
    fig = px.bar(
        top5,
        x='Location',
        y='New Recovered',
        color='New Recovered',
        color_continuous_scale='Blues',
        title="5 provinsi tertinggi dalam jumlah sembuh",
        labels={'Total Recovered':'Total Kesembuhan','Location':'Provinsi'}
    )
    fig.update_layout(xaxis_title='Provinsi',yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
         

def pie_chart(df):
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    data = {
        "Status": ["💀 Meninggal", "💚 Sembuh"],
        "Jumlah": [total_mati, total_sembuh]
    }

    fig = px.pie(
        data,
        names="Status",
        values="Jumlah",
        title="📊 Perbandingan Total Kematian VS Total Kesembuhan",
        hole=0.5,
        color_discrete_sequence=["#ff6459", "#4de89f"]
    )

    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    df['Date']= pd.to_datetime(df['Date'])

    if year :
        df =df[df['Date'].dt.year == year]

    df_agg = df.groupby(['Location','Latitude','Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset= ['Latitude','Longitude','New Cases'])

    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan dipeta")
        return 
    fig = px.scatter_mapbox(
        df_map,
        lat = 'Latitude',
        lon = 'Longitude',
        size = 'New Cases',
        color='New Cases',
        hover_name='Location',
        zoom=3,
        center={'lat':-2.5, "lon":118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale='OrRd',
        title=f"Sebaran kasus baru covid-19 diindonesia({year if year else 'Semua Tahun'})"
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={'r':0,'t':50,'l':0,'b':0}
    )
    st.plotly_chart(fig, use_container_width=True)