# -------------------------------------- Import Library ------------------------------
#Run using: streamlit run streamlit.py
import json
## Read Data and Preprocessing Data
import pandas as pd

## Visualization
import plotly.express as px 

## Dashboard 
import streamlit as st 

# ------------------------------ CONFIG ------------------------------
st.set_page_config(
    page_title="Analysis of 16,000+ Movies",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------- Read dataset ------------------------------
df = pd.read_pickle("movies.pkl")

# -------------------------------------- Membuat Sidebar ---------------------------

with st.sidebar:
    #Menambahkan logo pribadi
    st.write("Hello 👋")
    st.image("asset/data-science.png")
    st.write("""
            My name is Sophia! Here I present my final project for the Meraki Asa
             International Internship Program: Analysis of 16,000+ Movies using
             interactive visualizations. The data were taken from 
             from Metacritic. The ratings were made by user reviews. 
            """)
# -------------------------------------- ROW 1 ---------------------------
st.write("# Analysis of 16,000+ Movies on Metacritic")
st.write("""
         This analysis uses Python programming language and interactive
         visualization (Plotly Express). Data used are of 16,000 movies
         released between 1910 and 2024. Data were taken from:
         https://www.kaggle.com/datasets/kashifsahil/16000-movies-1910-2024-metacritic?resource=download&SSORegistrationToken=CfDJ8F_DuqmsDTJPtLCFEKPd8dxLWYFaOfTKmiMCsRWPNdfUgHq3l6mvLSZOW8CIkeYsihXny6ZHI6WL_PCtRDy_WCJAjyFmJWEssVRejoR3Zk6KysrxTzJVw2got603WWgn0l3iwvI3AkO5T3w2hLl8LyLIcARLj-yburnAuhIDVPgMq-he0cVUtwkKpJwmsH1KGxsj-SR4RG84Al79bAhNbsqyE4hZB0gX0jBZhTEfEhRaAjUtHmWhRBC5gdVus2vYIK-X3OvU_nJOGHjAda_kOAHxV_Z7Um_cGiSzhMzHdKOAkuIvnrpnvmZAOzXrIHqQQOqz06rTw8aBSQuGfZ8f-e4OJP8M&DisplayName=Sophia%20Fatima.
         """)
with st.expander("Click to see the dataset!"):
    st.write("Data on 16K+ Movies",df)

# -------------------------------------- ROW 2 ---------------------------
st.write("### 1. Are there any trends in (movie ratings, no of persons voted, duration) over time?")

# ---------- A. Filter Indicator
choices = st.radio("Pick One Indicator!",
         ("Rating", "No of Persons Voted", "Minutes"))

# ---------- B. Filter Date - Input Rentang Tanggal
min_date = df['Release Date'].min()
max_date = df['Release Date'].max()

# Input Data
start_date, end_date = st.date_input("Pick a Date Range!",
              value=[min_date,max_date],
              min_value=min_date,
              max_value=max_date)

# Ubah tipe data input date
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data
cond_min_max = (df['Release Date'] >= start_date) & (df['Release Date'] <= end_date)
filtered_df = df[cond_min_max]

# ---------- C. Persiapan Data
trend=filtered_df.groupby("Release Date")[choices].mean().reset_index()

# ---------- D. Visualisasi Data
fig_line=px.line(trend,
        x="Release Date",
        y=choices,
        title=f"The Average {choices} Over Time",
        markers=True,
        color_discrete_sequence=["skyblue"])

st.plotly_chart(fig_line)

# -------------------------------------- ROW 3 ---------------------------
st.write("### 2. Who are the top 10 directors with the highest average Ratings?")

# A. Input Data
rating_mean = df.groupby("Directed by")['Rating'].mean().reset_index() #reset_index membuat dataframe + merubah index menjadi kolom

# B. Visualisasi

#Top 10 Directors

fig_top10 = px.bar(rating_mean.sort_values(by="Rating", ascending=False)[:10],
         title="Top 10 Directors with Highest Average Ratings",
         x="Rating",
         y="Directed by",
         color_discrete_sequence=["skyblue"])

st.plotly_chart(fig_top10)

# -------------------------------------- ROW 4 ---------------------------
st.write("### 3. Who are the top 10 directors with the lowest average Ratings?")

# A. Input Data
rating_mean2 = df.groupby("Directed by")['Rating'].mean().reset_index() #reset_index membuat dataframe + merubah index menjadi kolom

# B. Visualisasi

#Top 10 Directors

fig_bottom10 = px.bar(rating_mean.sort_values(by="Rating", ascending=True)[:10],
         title="Top 10 Directors with Highest Average Ratings",
         x="Rating",
         y="Directed by",
         color_discrete_sequence=["skyblue"])

st.plotly_chart(fig_bottom10)

# -------------------------------------- ROW 5 ---------------------------

st.write("### 4. What is the impact of duration on ratings?")

# A. Persiapan Data

# B. Visualisasi
# Membuat scatter plot
scatter = px.scatter(x=df['Minutes'],
            y=df['Rating'],
            title="Relationship Between Duration of Film and Rating",
            color_discrete_sequence=["skyblue"],
            labels={'x':'Duration (minutes)', 'y':'Rating'}) #alpha is how thick the dots are

st.plotly_chart(scatter)



