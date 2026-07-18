import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD DATASET
# ==========================================================

df = pd.read_csv("netflix_titles.csv")

# ==========================================================
# DATA CLEANING
# ==========================================================

df["country"] = df["country"].fillna("Unknown")
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["rating"] = df["rating"].fillna(df["rating"].mode()[0])

# Movie duration
movies = df[df["type"] == "Movie"].copy()

movies["duration"] = (
    movies["duration"]
    .str.replace(" min", "", regex=False)
)

movies["duration"] = pd.to_numeric(
    movies["duration"],
    errors="coerce"
)

avg_duration = round(
    movies["duration"].mean(),
    1
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/7/75/Netflix_icon.svg",
    width=90
)

st.sidebar.title("🎬 Netflix Dashboard")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📂 Dataset Overview",

        "📊 EDA",

    ]

)

st.sidebar.markdown("---")

# ==========================================================
# GLOBAL FILTERS
# ==========================================================

st.sidebar.header("🎯 Global Filters")

selected_type = st.sidebar.multiselect(

    "Content Type",

    options=sorted(
        df["type"].dropna().unique()
    ),

    default=sorted(
        df["type"].dropna().unique()
    )

)

selected_rating = st.sidebar.multiselect(

    "Content Rating",

    options=sorted(
        df["rating"].dropna().unique()
    ),

    default=sorted(
        df["rating"].dropna().unique()
    )

)

selected_year = st.sidebar.slider(

    "Release Year",

    int(df["release_year"].min()),

    int(df["release_year"].max()),

    (

        int(df["release_year"].min()),

        int(df["release_year"].max())

    )

)

filtered_df = df[

    (df["type"].isin(selected_type))

    &

    (df["rating"].isin(selected_rating))

    &

    (

        df["release_year"].between(

            selected_year[0],

            selected_year[1]

        )

    )

]

st.sidebar.markdown("---")

st.sidebar.success(
    "Filters apply to all charts."
)
if page == "🏠 Home":
    st.title("🎬 Netflix Analytics Dashboard")
    st.subheader("A Data-Driven Analysis of Movies and TV Shows")

    st.markdown("---")

    st.write("""
This dashboard presents an Exploratory Data Analysis (EDA) of the Netflix Movies and TV Shows dataset.

It helps analyze Netflix's content library through interactive visualizations including content distribution, ratings, countries, release trends, genres and movie durations.

The dashboard is fully interactive and allows filtering the dataset to obtain meaningful insights.
""")
    st.markdown("---")

    # =====================================================
    # KPI CARDS
    # =====================================================

    total_titles = len(filtered_df)

    total_movies = (
        filtered_df["type"] == "Movie"
    ).sum()

    total_tv = (
        filtered_df["type"] == "TV Show"
    ).sum()

    total_country = (
        filtered_df["country"]
        .str.split(", ")
        .explode()
        .nunique()
    )

    movie_duration = filtered_df[
        filtered_df["type"] == "Movie"
    ].copy()

    movie_duration["duration"] = (
        movie_duration["duration"]
        .str.replace(" min","",regex=False)
    )

    movie_duration["duration"] = pd.to_numeric(
        movie_duration["duration"],
        errors="coerce"
    )

    avg_duration = round(
        movie_duration["duration"].mean(),
        1
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🎬 Total Titles", total_titles)
    c2.metric("🎥 Movies", total_movies)
    c3.metric("📺 TV Shows", total_tv)
    c4.metric("🌍 Countries", total_country)
    c5.metric("⏱ Avg Duration", f"{avg_duration} min")

    st.markdown("---")

    with st.container(border=True):

        st.subheader("🎯 Project Objectives")

        st.info("""

• Analyze Netflix Movies and TV Shows

• Perform Data Cleaning

• Perform Exploratory Data Analysis

• Discover Content Distribution

• Analyze Ratings

• Discover Top Producing Countries

• Analyze Release Trends

• Study Movie Duration
                
• Build Interactive Dashboard

""")

    st.markdown("")

    with st.container(border=True):

        st.subheader("🛠 Technologies Used")

        col1, col2 = st.columns(2)

        with col1:

            st.success("""

✔ Python

✔ Pandas

✔ NumPy

✔ Plotly

""")

        with col2:

            st.success("""

✔ Streamlit

✔ Matplotlib

✔ Seaborn

✔ Jupyter Notebook

""")

    st.markdown("---")

    with st.container(border=True):

        st.subheader("📂 Dataset Preview")

        st.dataframe(
            filtered_df.head(10),
            use_container_width=True
        )

    st.markdown("---")

    with st.container(border=True):

        st.subheader("📌 Dataset Information")

        st.write(f"""
**Dataset Name :** Netflix Movies and TV Shows

**Source :** Kaggle

**Total Records :** {len(df)}

**Total Columns :** {len(df.columns)}

**Content Types :** Movies and TV Shows

**Analysis Type :** Exploratory Data Analysis (EDA)
""")

    st.markdown("---")

    st.caption("Netflix Analytics Dashboard | Developed using Streamlit & Plotly")

elif page == "📂 Dataset Overview":
    st.title("📂 Dataset Overview")
    st.write("Understand the Netflix dataset before performing analysis.")

    st.markdown("---")

    # ======================================================
    # DATASET SUMMARY
    # ======================================================

    st.subheader("📊 Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(filtered_df))
    c2.metric("Columns", len(filtered_df.columns))
    c3.metric("Movies", (filtered_df["type"] == "Movie").sum())
    c4.metric("TV Shows", (filtered_df["type"] == "TV Show").sum())

    st.markdown("---")

    # ======================================================
    # DATASET PREVIEW
    # ======================================================

    with st.container(border=True):

        st.subheader("👀 Dataset Preview")

        rows = st.slider(
            "Select Number of Rows",
            5,
            50,
            10,
            key="preview_rows"
        )

        st.dataframe(
            filtered_df.head(rows),
            use_container_width=True
        )

    st.markdown("---")
    # ======================================================
    # DATASET INFORMATION
    # ======================================================
    with st.container(border=True):
        st.subheader("📋 Dataset Information")
        info = pd.DataFrame({
            "Column": filtered_df.columns,
            "Data Type": filtered_df.dtypes.astype(str),
            "Missing Values": filtered_df.isnull().sum().values
        })
        search = st.text_input("🔍 Search Movie")

        if search:
            st.dataframe(filtered_df[filtered_df["title"].str.contains(search, case=False, na=False)])
        else:
            st.dataframe(filtered_df)
        st.dataframe(
            info,
            use_container_width=True
        )
        st.download_button(
        "📥 Download Dataset",
        df.to_csv(index=False),
        "Netflix.csv",
        "text/csv"
        )

    st.markdown("---")
    # ======================================================
    # COLUMN DESCRIPTION
    # ======================================================
    with st.container(border=True):
        st.subheader("📖 Column Description")
        description = pd.DataFrame({

            "Column":[
                "show_id",
                "type",
                "title",
                "director",
                "cast",
                "country",
                "date_added",
                "release_year",
                "rating",
                "duration",
                "listed_in",
                "description"
            ],

            "Meaning":[
                "Unique ID of every Netflix title",
                "Movie or TV Show",
                "Title of the content",
                "Director name",
                "Cast members",
                "Country of production",
                "Date added on Netflix",
                "Original release year",
                "Age certification",
                "Movie duration or TV seasons",
                "Genre/category",
                "Brief summary"
            ]

        })

        st.dataframe(
            description,
            use_container_width=True
        )

    st.markdown("---")

    # ======================================================
    # STATISTICAL SUMMARY
    # ======================================================

    with st.container(border=True):

        st.subheader("📈 Statistical Summary")

        st.dataframe(
            filtered_df.describe(include="all"),
            use_container_width=True
        )

    st.markdown("---")

    # ======================================================
    # DATA CLEANING SUMMARY
    # ======================================================

    with st.expander("🧹 Data Cleaning Performed"):

        st.success("""

✔ Filled missing values in Country

✔ Filled missing values in Director

✔ Filled missing values in Cast

✔ Filled missing values in Rating

✔ Converted Movie Duration into numeric format

✔ Removed invalid duration values

✔ Applied global filters for dashboard

""")
elif page == "📊 EDA":
        # ==========================================================
    # EDA PAGE
    # ==========================================================

    st.title("📊 Exploratory Data Analysis")
    st.write(
        "Explore Netflix Movies and TV Shows using interactive Plotly visualizations."
    )

    st.markdown("---")

    # ==========================================================
    # EDA FILTERS
    # ==========================================================

    with st.expander("🎯 Chart Filters", expanded=True):

        chart_type = st.multiselect(
            "Select Content Type",
            options=sorted(filtered_df["type"].unique()),
            default=sorted(filtered_df["type"].unique()),
            key="eda_type"
        )

        chart_df = filtered_df[
            filtered_df["type"].isin(chart_type)
        ]

    st.markdown("---")

    # ======
    # KPI CARDS
    total_titles = len(filtered_df)
    total_movies = len(filtered_df[filtered_df["type"] == "Movie"])
    total_tv = len(filtered_df[filtered_df["type"] == "TV Show"])
    total_countries = (filtered_df["country"]
        .str.split(", ")
        .explode()
        .nunique()
    )

    total_ratings = filtered_df["rating"].nunique()
    total_genres = (
        filtered_df["listed_in"]
        .str.split(", ")
        .explode()
        .nunique()
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("🎬 Total Titles", total_titles)
    c2.metric("🎥 Movies", total_movies)
    c3.metric("📺 TV Shows", total_tv)
    c4.metric("🌍 Countries", total_countries)
    c5.metric("⭐ Ratings", total_ratings)
    c6.metric("🎭 Genres", total_genres)
    st.markdown("---")
    # ==========================================================
    # TABS
    # ==========================================================
    tab1, tab2, tab3, tab4, tab5= st.tabs(
        [
            "📈 Overview",
            "🌍 Geography",
            "🎭 Content",
            "👥 director & cast",
            "📊 Advance"
        ]
    )
    # ==========================================================
    # TAB 1 : OVERVIEW
    # ==========================================================
    with tab1:
        st.header("📈 Netflix Content Overview")
        with st.container(border=True):
            st.subheader("🥧 Distribution of Movies and TV Shows")
            content = (
                chart_df["type"]
                .value_counts()
                .reset_index())

            content.columns = ["Type", "Titles"]

            fig = px.pie(
                content,
                names="Type",
                values="Titles",
                color="Type",
                color_discrete_map={
                    "Movie": "#E50914",
                    "TV Show": "#2A9D8F"})
            
            fig.update_traces(

                textinfo="label+percent",

                textfont=dict(
                    size=16,
                    color="black",
                    family="Arial Black"
                ),

                marker=dict(
                    line=dict(
                        color="black",
                        width=2
                    )
                ),

                pull=[0.08, 0.03],

                hovertemplate=
                "<b>%{label}</b><br>"
                "Titles : %{value}<br>"
                "Percentage : %{percent}<extra></extra>"
            )

            fig.update_layout(

                template="plotly_white",

                paper_bgcolor="white",

                plot_bgcolor="white",

                title=dict(
                    text="<b>Distribution of Movies and TV Shows</b>",
                    x=0.5,
                    font=dict(
                        size=22,
                        color="black",
                        family="Arial Black"
                    )
                ),

                font=dict(
                    color="black",
                    family="Arial Black",
                    size=13
                ),

                legend=dict(
                    title="<b>Content Type</b>",
                    font=dict(
                        color="black",
                        family="Arial Black"
                    )
                ),

                margin=dict(
                    l=40,
                    r=40,
                    t=80,
                    b=40
                ),

                height=550
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="pie_chart"
            )
            st.info("""
            **Insight**

            📌 Insights
            Netflix's library is dominated by Movies, making up around 70% of all titles.
            TV Shows account for approximately 30%, but their presence has grown steadily over time.
            This indicates that Netflix has historically focused more on films while increasingly investing in original TV series.""")

        st.markdown("---")

        # ======================================================
        # LINE CHART
        # ======================================================

        with st.container(border=True):

            st.subheader("📈 Movies vs TV Shows Released Over Years")

            trend = (

                chart_df

                .groupby(
                    ["release_year", "type"]
                )

                .size()

                .reset_index(name="Titles")

            )

            fig = px.line(

                trend,

                x="release_year",

                y="Titles",

                color="type",

                markers=True,

                color_discrete_map={

                    "Movie": "#E50914",

                    "TV Show": "#2A9D8F"

                }

            )

            fig.update_traces(

                line=dict(width=4),

                marker=dict(
                    size=8,
                    line=dict(
                        color="black",
                        width=1
                    )
                )

            )

            fig.update_layout(

                template="plotly_white",

                paper_bgcolor="white",

                plot_bgcolor="white",

                title=dict(

                    text="<b>Movies vs TV Shows Released Over the Years</b>",

                    x=0.5,

                    font=dict(
                        size=22,
                        color="black",
                        family="Arial Black"
                    )

                ),

                xaxis=dict(

                    title="<b>Release Year</b>",

                    tickfont=dict(
                        color="black",
                        family="Arial Black"
                    ),

                    title_font=dict(
                        color="black",
                        family="Arial Black",
                        size=16
                    ),

                    gridcolor="lightgray",

                    linecolor="black",

                    mirror=True

                ),

                yaxis=dict(

                    title="<b>Number of Titles</b>",

                    tickfont=dict(
                        color="black",
                        family="Arial Black"
                    ),

                    title_font=dict(
                        color="black",
                        family="Arial Black",
                        size=16
                    ),

                    gridcolor="lightgray",

                    linecolor="black",

                    mirror=True

                ),

                legend=dict(

                    title="<b>Content Type</b>",

                    font=dict(
                        color="black",
                        family="Arial Black"
                    )

                ),

                font=dict(
                    color="black",
                    family="Arial Black"
                ),

                height=550

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="line_chart"
            )
            
            st.info(""" 
            📌 Insights
                    
            Netflix content increased rapidly after 2015.
            Movie releases remain higher than TV Show releases throughout most years.
            The growth reflects Netflix's expansion into original productions and international content.""")
                    
    # ==========================================================
    # TAB 2 : GEOGRAPHY
    # ==========================================================

    with tab2:

        st.header("🌍 Geographic Analysis")

        # ======================================================
        # CONTENT RATINGS
        # ======================================================

        with st.container(border=True):

            st.subheader("📊 Netflix Content Ratings by Type")

            rating_data = (
                chart_df
                .groupby(["rating", "type"])
                .size()
                .reset_index(name="Titles")
            )

            fig = px.bar(

                rating_data,

                x="rating",

                y="Titles",

                color="type",

                text="Titles",

                barmode="group",

                color_discrete_map={

                    "Movie": "#E50914",

                    "TV Show": "#2A9D8F"

                }

            )

            fig.update_traces(

                marker_line_color="black",

                marker_line_width=1.5,

                textposition="outside",

                textfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                )

            )

            fig.update_layout(

                template="plotly_white",

                title=dict(

                    text="<b>Netflix Content Ratings by Type</b>",

                    x=0.5,

                    font=dict(

                        size=22,

                        color="black",

                        family="Arial Black"

                    )

                ),

                paper_bgcolor="white",

                plot_bgcolor="white",

                font=dict(

                    color="black",

                    family="Arial Black"

                ),

                xaxis=dict(

                    title="<b>Content Rating</b>",

                    tickfont=dict(

                        color="black",

                        family="Arial Black"

                    ),

                    title_font=dict(

                        color="black",

                        family="Arial Black",
                        size=15
                    ),

                    linecolor="black",

                    mirror=True

                ),

                yaxis=dict(

                    title="<b>Number of Titles</b>",

                    tickfont=dict(

                        color="black",

                        family="Arial Black"

                    ),

                    title_font=dict(

                        color="black",

                        family="Arial Black",

                        size=15

                    ),

                    gridcolor="lightgray",

                    linecolor="black",

                    mirror=True

                ),

                legend=dict(

                    title="<b>Content Type</b>",

                    font=dict(

                        color="black",

                        family="Arial Black"

                    )

                ),

                height=550

            )

            st.plotly_chart(

                fig,

                use_container_width=True,

                key="rating_chart"

            )
            st.info("""
            📌 Insights
                    
            TV-MA is the most common rating, indicating a strong focus on mature audiences.
            TV-14 and PG-13 are also widely represented.
            Movies are available across a broader range of ratings than TV Shows""")
        st.markdown("---")

        # ======================================================
        # TOP COUNTRIES
        # ======================================================

        with st.container(border=True):

            st.subheader("🌍 Top 10 Countries Producing Netflix Content")

            country_df = chart_df.copy()

            country_df = country_df.dropna(subset=["country"])

            country_df["country"] = country_df["country"].str.split(", ")

            country_df = country_df.explode("country")

            country_df = country_df[
                country_df["country"].str.lower() != "unknown"
            ]

            top10 = (
                country_df["country"]
                .value_counts()
                .head(10)
                .index
            )

            country_top = (
                country_df[
                    country_df["country"].isin(top10)
                ]
                .groupby(["country", "type"])
                .size()
                .reset_index(name="Titles")
            )

            fig = px.bar(

                country_top,

                x="Titles",

                y="country",

                orientation="h",

                color="type",

                text="Titles",

                barmode="group",

                category_orders={
                    "country": list(top10[::-1])
                },

                color_discrete_map={
                    "Movie": "#E50914",
                    "TV Show": "#2A9D8F"
                }

            )

            fig.update_traces(

                marker_line_color="black",

                marker_line_width=1.5,

                textposition="outside",

                textfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                )

            )

            fig.update_layout(

                template="plotly_white",

                title=dict(

                    text="<b>Top 10 Countries Producing Netflix Content</b>",

                    x=0.5,

                    font=dict(

                        size=22,

                        color="black",

                        family="Arial Black"

                    )

                ),

                paper_bgcolor="white",

                plot_bgcolor="white",

                font=dict(

                    color="black",

                    family="Arial Black"

                ),

                xaxis=dict(

                    title="<b>Number of Titles</b>",

                    tickfont=dict(

                        color="black",

                        family="Arial Black"

                    ),

                    title_font=dict(

                        color="black",

                        family="Arial Black",

                        size=15

                    ),

                    gridcolor="lightgray",

                    linecolor="black",

                    mirror=True

                ),

                yaxis=dict(

                    title="<b>Country</b>",

                    tickfont=dict(

                        color="black",

                        family="Arial Black"

                    ),

                    title_font=dict(

                        color="black",

                        family="Arial Black",

                        size=15

                    ),

                    linecolor="black",

                    mirror=True

                ),

                legend=dict(

                    title="<b>Content Type</b>",

                    font=dict(

                        color="black",

                        family="Arial Black"

                    )

                ),

                height=650

            )

            st.plotly_chart(

                fig,

                use_container_width=True,

                key="country_chart"

            )
            st.info("""
            📌 Insights
                    
            The United States contributes the highest number of Netflix titles.
            India ranks second, highlighting its strong film industry.
            Countries such as the United Kingdom, Canada, Japan, and South Korea also make significant contributions.
            Netflix has a diverse international catalogue.""")        
        # ==========================================================
    # TAB 3 : CONTENT ANALYSIS
    # ==========================================================
    with tab3:
        st.header("🎭 Content Analysis")
        with st.container(border=True):
            st.subheader("🎭 Top 10 Netflix Genres")

            genre_df = chart_df.copy()

            genre_df["listed_in"] = genre_df["listed_in"].str.split(", ")

            genre_df = genre_df.explode("listed_in")

            top_genres = (
                genre_df.groupby("listed_in")["show_id"]
                .count()
                .sort_values(ascending=False)
                .head(10)
                .reset_index(name="Titles")
            )

            fig = px.bar(
                top_genres,
                x="Titles",
                y="listed_in",
                orientation="h",
                text="Titles",
                color="Titles",
                color_continuous_scale="Teal"
            )

            fig.update_traces(

                marker_line_color="black",
                marker_line_width=1.8,

                textposition="outside",

                textfont=dict(
                    color="black",
                    size=12,
                    family="Arial Black"
                )

            )

            fig.update_layout(

                template="plotly_white",

                paper_bgcolor="white",
                plot_bgcolor="white",

                coloraxis_showscale=False,

                title=dict(
                    text="<b>Top 10 Netflix Genres</b>",
                    x=0.5,
                    font=dict(
                        size=22,
                        color="black"
                    )
                ),

                font=dict(
                    color="black",
                    family="Arial Black",
                    size=13
                ),

                xaxis=dict(

                    title="<b>Number of Titles</b>",

                    title_font=dict(color="black", size=15),

                    tickfont=dict(color="black"),

                    linecolor="black",

                    mirror=True,

                    gridcolor="lightgray"

                ),

                yaxis=dict(

                    title="<b>Genre</b>",

                    title_font=dict(color="black", size=15),

                    tickfont=dict(color="black"),

                    linecolor="black",

                    mirror=True

                ),

                height=600

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="genre_plot"
            )
            st.info("""
            📌 Insights
                    
            International Movies represent the largest genre.
            Dramas and Comedies are among the most popular categories.
            Netflix emphasizes content variety to appeal to different audience preferences.""")
        st.markdown("---")

        with st.container(border=True):

            st.subheader("📅 Years Taken to Add Content to Netflix")

            df_hist = chart_df[
                chart_df["release_year"] >= 2007
            ].copy()

            df_hist["date_added"] = pd.to_datetime(
                df_hist["date_added"],
                errors="coerce"
            )

            df_hist["years_to_netflix"] = (
                df_hist["date_added"].dt.year
                - df_hist["release_year"]
            )

            df_hist = df_hist[
                df_hist["years_to_netflix"] >= 0
            ]

            fig = px.histogram(

                df_hist,

                x="years_to_netflix",

                nbins=15,

                color_discrete_sequence=["steelblue"]

            )

            fig.update_traces(

                marker_line_color="black",

                marker_line_width=1.6

            )

            fig.update_layout(

                template="plotly_white",

                paper_bgcolor="white",

                plot_bgcolor="white",

                title=dict(

                    text="<b>Distribution of Years Taken to Add Content to Netflix (2007+)</b>",

                    x=0.5,

                    font=dict(
                        color="black",
                        size=20
                    )

                ),

                font=dict(
                    color="black",
                    family="Arial Black"
                ),

                xaxis=dict(

                    title="<b>Years Between Release and Netflix Addition</b>",

                    title_font=dict(
                        color="black",
                        size=15
                    ),

                    tickfont=dict(color="black"),

                    linecolor="black",

                    mirror=True

                ),

                yaxis=dict(

                    title="<b>Number of Titles</b>",

                    title_font=dict(
                        color="black",
                        size=15
                    ),

                    tickfont=dict(color="black"),

                    linecolor="black",

                    mirror=True,

                    gridcolor="lightgray"

                ),

                height=550

            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="hist_plot"
            )
            st.info("""
            📌 Insights
                    
            Most content is added to Netflix within 0–3 years after its original release.
            Only a small number of older titles are added much later.
            Netflix prioritizes recently released content to keep its catalogue current.""")
 # ==========================================================
# TAB 4 : PEOPLE ANALYSIS
# ==========================================================
    with tab4:
        st.header("👥 People Analysis")
        with st.container(border=True):
            st.subheader("🎬 Top 10 Directors with Most Netflix Titles")

        director_df = chart_df.copy()

        director_df = director_df.dropna(subset=["director"])

        director_df["director"] = (
            director_df["director"]
            .str.split(", ")
        )

        director_df = director_df.explode("director")

        director_df = director_df[
            (director_df["director"] != "") &
            (director_df["director"] != "Unknown") &
            (director_df["director"] != "Not Available")
        ]

        top_directors = (

            director_df

            .groupby("director")["show_id"]

            .count()

            .sort_values(ascending=False)

            .head(10)

            .sort_values()

            .reset_index(name="Titles")

        )

        fig = px.bar(

            top_directors,

            x="Titles",

            y="director",

            orientation="h",

            text="Titles",

            color="Titles",

            color_continuous_scale="Reds"

        )

        fig.update_traces(

            marker_line_color="black",

            marker_line_width=2,

            textposition="outside",

            cliponaxis=False,

            textfont=dict(

                color="black",

                size=12,

                family="Arial Black"

            )

        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            coloraxis_showscale=False,

            title=dict(
                text="<b>Top 10 Directors with Most Netflix Titles</b>",
                x=0.5,

                font=dict(
                    color="black",
                    size=22,
                    family="Arial Black"

                )

            ),

            font=dict(
                color="black",
                family="Arial Black",
                size=13
            ),

            margin=dict(
                l=250,
                r=40,
                t=80,
                b=70
            ),

            xaxis=dict(

                title=dict(

                    text="<b>Number of Titles</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                ),

                showline=True,

                linecolor="black",

                linewidth=2,

                mirror=True,

                ticks="outside",

                showgrid=True,

                gridcolor="lightgray"

            ),

            yaxis=dict(

                title=dict(

                    text="<b>Director</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                ),

                automargin=True,

                showline=True,

                linecolor="black",

                linewidth=2,

                mirror=True

            ),

            height=650

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            key="director_chart"

        )
        st.info("""
        📌 Insights
                
        A small group of directors contributes a significant number of titles.
        Frequent collaborations with these directors indicate strong professional partnerships.
        This suggests Netflix values experienced and successful filmmakers.""")
        st.markdown("---")

        with st.container(border=True):

            st.subheader("👤 Top 10 Most Frequently Appearing Actors")

        cast_df = chart_df.copy()

        cast_df = cast_df.dropna(subset=["cast"])

        cast_df["cast"] = (
            cast_df["cast"]
            .str.split(", ")
        )

        cast_df = cast_df.explode("cast")

        cast_df = cast_df[
            (cast_df["cast"] != "") &
            (cast_df["cast"] != "Unknown") &
            (cast_df["cast"] != "Not Available")
        ]

        top_cast = (

            cast_df

            .groupby("cast")["show_id"]

            .count()

            .sort_values(ascending=False)

            .head(10)

            .sort_values()

            .reset_index(name="Titles")

        )

        fig = px.bar(

            top_cast,

            x="Titles",

            y="cast",

            orientation="h",

            text="Titles",

            color="Titles",

            color_continuous_scale="Oranges"

        )

        fig.update_traces(

            marker_line_color="black",

            marker_line_width=2,

            textposition="outside",

            cliponaxis=False,

            textfont=dict(

                color="black",

                size=12,

                family="Arial Black"

            )

        )

        fig.update_layout(

            template="plotly_white",

            paper_bgcolor="white",

            plot_bgcolor="white",

            coloraxis_showscale=False,

            title=dict(

                text="<b>Top 10 Most Frequently Appearing Actors</b>",

                x=0.5,

                font=dict(

                    color="black",

                    size=22,

                    family="Arial Black"

                )

            ),

            font=dict(

                color="black",

                family="Arial Black",

                size=13

            ),

            margin=dict(

                l=250,

                r=40,

                t=80,

                b=70

            ),

            xaxis=dict(

                title=dict(

                    text="<b>Number of Titles</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                ),

                showline=True,

                linecolor="black",

                linewidth=2,

                mirror=True,

                ticks="outside",

                showgrid=True,

                gridcolor="lightgray"

            ),

            yaxis=dict(

                title=dict(

                    text="<b>Actor</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=12,

                    family="Arial Black"

                ),

                automargin=True,

                showline=True,

                linecolor="black",

                linewidth=2,

                mirror=True

            ),

            height=650

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            key="actor_chart"

        )
        st.info("""
        📌 Insights
                
        Several actors appear repeatedly across Netflix titles.
        Frequent appearances indicate strong audience appeal and recurring collaborations.
        Popular actors help attract viewers and strengthen Netflix's content portfolio. """)
    # ==========================================================
# TAB 5 : ADVANCED ANALYSIS
# ==========================================================

    with tab5:
        st.header("📊 Advanced Analysis")
        with st.container(border=True):
            st.subheader("🔥 Average Movie Duration by Rating and Release Year")

        movies = chart_df[
            chart_df["type"] == "Movie"
        ].copy()

        movies["duration"] = (
            movies["duration"]
            .str.replace(" min", "", regex=False)
        )

        movies["duration"] = pd.to_numeric(
            movies["duration"],
            errors="coerce"
        )

        movies = movies.dropna(subset=["duration"])

        pivot = movies.pivot_table(

            values="duration",

            index="rating",

            columns="release_year",

            aggfunc="mean"

        )

        fig = px.imshow(

            pivot,

            color_continuous_scale="Viridis",

            aspect="auto",

            text_auto=".0f"

        )

        fig.update_layout(

            template="plotly_white",

            paper_bgcolor="white",

            plot_bgcolor="white",

            title=dict(

                text="<b>Average Movie Duration by Rating and Release Year</b>",

                x=0.5,

                font=dict(

                    color="black",

                    size=22,

                    family="Arial Black"

                )

            ),

            font=dict(

                color="black",

                family="Arial Black",

                size=13

            ),

            margin=dict(

                l=120,

                r=40,

                t=80,

                b=80

            ),

            xaxis=dict(

                title=dict(

                    text="<b>Release Year</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=11,

                    family="Arial Black"

                ),

                showline=True,

                linewidth=2,

                linecolor="black",

                mirror=True

            ),

            yaxis=dict(

                title=dict(

                    text="<b>Content Rating</b>",

                    font=dict(

                        color="black",

                        size=16,

                        family="Arial Black"

                    )

                ),

                tickfont=dict(

                    color="black",

                    size=11,

                    family="Arial Black"

                ),

                showline=True,

                linewidth=2,

                linecolor="black",

                mirror=True,

                automargin=True

            ),

            height=700

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            key="heatmap"

        )
        st.info("""
        📌 Insights
        
        Average movie duration varies across both release years and content ratings.
        Certain rating categories consistently feature longer movies.
        The heatmap helps identify trends that are difficult to observe using traditional charts.""")
        st.markdown("---")

    # -------------------------------------------------------
    # Movie Duration Box Plot
    # -------------------------------------------------------

        st.markdown("---")
        with st.container(border=True):
            st.subheader("🎬 Movie Duration by Content Rating")

            movies = filtered_df[filtered_df["type"] == "Movie"].copy()
            movies["duration"] = ( movies["duration"].str.replace(" min", "", regex=False))

            movies["duration"] = pd.to_numeric( movies["duration"],errors="coerce")
            movies = movies.dropna(subset=["duration"])

            top_ratings = ( movies["rating"].value_counts().head(6).index)
            movies = movies[movies["rating"].isin(top_ratings)]
            fig = px.box( movies,x="rating",y="duration",points="outliers")

            fig.update_traces(fillcolor="#E50914",opacity=0.85,
                line=dict(color="black",width=2),

            marker=dict(color="black",size=5,
                line=dict(color="black",width=1)))

            fig.update_layout(

                template="plotly_white",

                paper_bgcolor="white",

                plot_bgcolor="white",

            title=dict(

                text="<b>Movie Duration by Content Rating</b>",

                x=0.5,

                font=dict(

                family="Arial Black",

                size=22,

                color="black"

            )

        ),

        font=dict(

            family="Arial Black",

            size=13,

            color="black"

        ),

        xaxis=dict(

            title="<b>Content Rating</b>",

            title_font=dict(

                family="Arial Black",

                size=16,

                color="black"

            ),

            tickfont=dict(

                family="Arial Black",

                size=12,

                color="black"

            ),

            showline=True,

            linewidth=2,

            linecolor="black",

            mirror=True

            ),

            yaxis=dict(

                title="<b>Duration (Minutes)</b>",

                title_font=dict(

                family="Arial Black",

                size=16,

                color="black"

            ),

                tickfont=dict(

                family="Arial Black",

                size=12,

                color="black"),

            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True,
            gridcolor="lightgray"),
            height=650,
            margin=dict(l=80,r=40,t=80,b=70),
            showlegend=False)
            st.plotly_chart(fig,use_container_width=True,key="movie_duration_box")

        st.info("""
        📌 Insights        
                
        Most movies have durations between 90 and 120 minutes.
        Higher-rated categories such as TV-MA show greater variation in runtime.
        Outliers represent exceptionally short or long movies""")    