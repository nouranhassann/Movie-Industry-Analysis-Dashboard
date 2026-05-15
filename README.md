🎬 Movie Industry Analysis Dashboard
📌 Project Overview

This project analyzes the movie industry using the TMDB 5000 Movie Dataset.
It explores key factors that influence movie success such as ratings, budgets, revenues, genres, runtimes, production companies, and languages.

The goal is to build an interactive analytics dashboard that helps uncover what makes a movie successful and how the industry has evolved over time.

🎯 Objectives
Analyze movie ratings, revenue, and budget trends
Compare performance across genres, languages, and production companies
Investigate the relationship between budget vs box office revenue
Study distribution of:
Ratings
Runtimes
Revenues
Track how the movie industry evolved over the years
Identify patterns behind successful movies
📊 Dataset
Name: TMDB 5000 Movie Dataset
Source: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
Size: ~5,000 movies
Main Features Used:
budget
revenue
genres
vote_average
vote_count
runtime
release_date
production_companies
original_language
🧹 Data Preprocessing

A preprocessing pipeline was created to clean and prepare the dataset:

Steps Included:
Handling missing values
Converting data types (dates, numeric fields)
Extracting useful features from JSON-like columns (genres, companies)
Removing irrelevant or corrupted entries
Creating new features such as:
Profit = Revenue - Budget
Profit Margin
Release Year
Standardizing categorical data
📈 Analysis & Insights

The project focuses on answering key business questions like:

Which genres generate the highest revenue?
Do higher budgets guarantee higher profits?
What is the relationship between runtime and rating?
Which production companies dominate the industry?
How has movie production changed over time?
🧰 Tools & Technologies
Python 🐍
Pandas
NumPy
Matplotlib / Seaborn
Jupyter Notebook
Power BI / Streamlit (if used for dashboard)
📊 Dashboard Features

The final dashboard includes:

Revenue vs Budget analysis
Genre performance comparison
Ratings distribution
Time-series trends of movie production
Top movies / companies analysis
Interactive filters (year, genre, language)

💡 Key Takeaway
This project shows how data analytics can uncover meaningful insights from the entertainment industry and help understand what drives a movie’s success
