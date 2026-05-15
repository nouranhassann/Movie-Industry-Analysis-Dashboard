"""
Charts.py — Movie Industry Analysis Dashboard
All reusable chart functions.

Guidelines (Color Strategy):
  - Column / Bar charts     : BASE_BAR_COLOR for all bars; WINNER_COLOR for highest/lowest bar.
  - Stacked charts          : Tonal shades of one hue (light → dark). No winner bar.
                              For categorical segments use semantic colors (red/amber/green).
  - Clustered charts        : Two distinct colors — one per metric (CLUSTER_A, CLUSTER_B).
                              No winner highlighting; goal is cross-group comparison.
  - template="plotly_white" on every chart (white background).
  - All chart titles and axis labels use black (Georgia serif).
  - Legends visible on every chart.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# Colour palette
# ─────────────────────────────────────────────
BASE_BAR_COLOR  = "#5B9BD5"   # steel-blue  — regular bars (column / bar)
WINNER_COLOR    = "#1CE666"   # green       — highest / winner bar (simple column/bar)
WINNER_DARK     = "#295e90"   # dark blue   — reserved accent

# Stacked charts — tonal shades of the same hue
STACK_LIGHT     = "#80C1FF"   # light blue  — first segment  (e.g. Budget)
STACK_DARK      = "#5B9BD5"   # steel blue  — second segment (e.g. Profit)

# Winner bin colors for stacked / clustered charts (green family)
WINNER_GREEN       = "#22A045"   # dark green  — winner bin (dominant segment)
WINNER_LIGHT_GREEN = "#6DD97A"   # light green — winner bin (secondary segment)

# Clustered charts — two harmonious, distinct colors (one per metric)
CLUSTER_A       = "#5B9BD5"   # steel blue  — first metric
CLUSTER_B       = "#80C1FF"   # light blue  — second metric

ACCENT_COLORS   = px.colors.qualitative.Set2

LAYOUT_DEFAULTS = dict(
    template      = "plotly_white",
    title_x       = 0.5,
    title_font    = dict(size=16, family="Georgia, serif", color="black"),
    font          = dict(family="Georgia, serif", size=12, color="black"),
    paper_bgcolor = "white",
    plot_bgcolor  = "white",
)


# ─────────────────────────────────────────────
# WEEK 1 — Column Chart  (vertical bars)
# Top 10 Genres by Average Revenue
# ─────────────────────────────────────────────
def genre_revenue_chart(df):
    grouped = (df.groupby("main_genre")["revenue"]
                 .mean()
                 .reset_index()
                 .sort_values("revenue", ascending=False)
                 .head(10))

    colors = [WINNER_COLOR if i == 0 else BASE_BAR_COLOR
              for i in range(len(grouped))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x            = grouped["main_genre"],
        y            = grouped["revenue"],
        marker_color = colors,
        text         = grouped["revenue"].apply(lambda v: f"${v/1e6:.1f}M"),
        textposition = "outside",
        showlegend   = False,
        name         = "Average Revenue",
    ))
    # Dummy traces for legend colour keys
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=WINNER_COLOR,
                         name="Highest Revenue Genre", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=BASE_BAR_COLOR,
                         name="Other Genres", showlegend=True))

    fig.update_layout(
        title       = "Top 10 Genres by Average Box-Office Revenue (Column Chart)",
        xaxis_title = "Genre",
        yaxis_title = "Average Revenue (USD)",
        legend      = dict(orientation="v", yanchor="top", y=1,
                           xanchor="left", x=1.01,
                           bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 1 — Bar Chart  (horizontal bars)
# Top 10 Production Companies by Average Runtime
# ─────────────────────────────────────────────
def runtime_by_company_chart(df):
    grouped = (df.groupby("main_company")["runtime"]
                 .mean()
                 .reset_index()
                 .sort_values("runtime", ascending=True)
                 .tail(10))

    colors = [WINNER_COLOR if i == len(grouped) - 1 else BASE_BAR_COLOR
              for i in range(len(grouped))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y            = grouped["main_company"],
        x            = grouped["runtime"],
        orientation  = "h",
        marker_color = colors,
        text         = grouped["runtime"].apply(lambda v: f"{v:.0f} min"),
        textposition = "outside",
        showlegend   = False,
        name         = "Average Runtime",
    ))
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h",
                         marker_color=WINNER_COLOR,
                         name="Longest Runtime Company", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h",
                         marker_color=BASE_BAR_COLOR,
                         name="Other Companies", showlegend=True))

    fig.update_layout(
        title       = "Top 10 Production Companies by Average Runtime (Bar Chart)",
        xaxis_title = "Average Runtime (minutes)",
        yaxis_title = "Production Company",
        legend      = dict(orientation="v", yanchor="top", y=1,
                           xanchor="left", x=1.01,
                           bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 2 — Stacked Column Chart
# Total Budget vs Profit by Genre
# Color rule: tonal shades of one hue — no winner bar
# ─────────────────────────────────────────────
def stacked_revenue_chart(df):
    grouped = (df.groupby("main_genre")[["budget", "profit"]]
                 .sum()
                 .head(10)
                 .reset_index())
    grouped["total"] = grouped["budget"] + grouped["profit"]
    grouped = grouped.sort_values("total", ascending=False)

    # Winner = genre with the highest total stack (index 0 after sort descending)
    budget_colors = [WINNER_LIGHT_GREEN if i == 0 else STACK_LIGHT for i in range(len(grouped))]
    profit_colors = [WINNER_GREEN       if i == 0 else STACK_DARK  for i in range(len(grouped))]

    fig = go.Figure()
    # Real data traces — showlegend=False; legend handled by dummy traces below
    fig.add_trace(go.Bar(
        x            = grouped["main_genre"],
        y            = grouped["budget"],
        name         = "Budget",
        marker_color = budget_colors,
        showlegend   = False,
    ))
    fig.add_trace(go.Bar(
        x            = grouped["main_genre"],
        y            = grouped["profit"],
        name         = "Profit",
        marker_color = profit_colors,
        showlegend   = False,
    ))

    # Dummy legend entries — blues first (others), greens second (winner)
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=STACK_DARK,
                         name="Profit (Other Genres)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=STACK_LIGHT,
                         name="Budget (Other Genres)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=WINNER_GREEN,
                         name="Profit — Highest Genre (Winner)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=WINNER_LIGHT_GREEN,
                         name="Budget — Highest Genre (Winner)", showlegend=True))

    fig.update_layout(
        barmode      = "stack",
        title        = "Total Budget vs Profit by Genre (Stacked Column Chart)",
        xaxis_title  = "Genre",
        yaxis_title  = "Amount (USD)",
        legend_title = "Revenue Component",
        legend       = dict(orientation="v", yanchor="top", y=1,
                            xanchor="left", x=1.01,
                            bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 2 — Stacked Bar Chart  (horizontal)
# Ratings Distribution Across Top Languages
# Color rule: semantic colors (red=Low, amber=Average, green=High)
# ─────────────────────────────────────────────
def ratings_language_stacked_bar(df):
    dff = df.copy()
    bins   = [0, 5, 7.5, 10]
    labels = ["Low (0–5)", "Average (5–7.5)", "High (7.5–10)"]
    dff["rating_category"] = pd.cut(
        dff["vote_average"], bins=bins, labels=labels, include_lowest=True)

    top_langs = dff["original_language"].value_counts().head(10).index
    dff = dff[dff["original_language"].isin(top_langs)]

    grouped = (dff.groupby(["original_language", "rating_category"])
                  .size()
                  .reset_index(name="count"))

    fig = px.bar(
        grouped,
        y           = "original_language",
        x           = "count",
        color       = "rating_category",
        orientation = "h",
        barmode     = "stack",
        title       = "Ratings Distribution Across Top Languages (Stacked Bar Chart)",
        category_orders = {"rating_category": labels},
        color_discrete_map = {
            "Low (0–5)":       "#A6CFF5",
            "Average (5–7.5)": "#80C1FF",
            "High (7.5–10)":   "#5B9BD5",
        },
        labels = {
            "original_language": "Language",
            "count": "Number of Movies",
            "rating_category": "Rating Category",
        }
    )
    fig.update_layout(
        yaxis = {"categoryorder": "total ascending"},
        legend       = dict(orientation="v", yanchor="top", y=1,
                            xanchor="left", x=1.01,
                            bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 2 — Clustered Column Chart
# Avg Budget vs Revenue per Year (last 20 years)
# Color rule: CLUSTER_A for Budget, CLUSTER_B for Revenue — no winner bar
# ─────────────────────────────────────────────
def budget_revenue_year_clustered_column(df):
    dff = df.copy()
    dff["year"] = pd.to_datetime(dff["release_date"], errors="coerce").dt.year
    dff = dff.dropna(subset=["year"])
    recent = sorted(dff["year"].unique())[-20:]
    dff    = dff[dff["year"].isin(recent)]

    grouped = dff.groupby("year")[["budget", "revenue"]].mean().reset_index().head(10)

    # Winner = year with the highest average revenue — sort it to the far LEFT (first position)
    winner_year = grouped.loc[grouped["revenue"].idxmax(), "year"]
    winner_row  = grouped[grouped["year"] == winner_year]
    others      = grouped[grouped["year"] != winner_year].sort_values("year")
    grouped     = pd.concat([winner_row, others], ignore_index=True)

    budget_colors  = [WINNER_LIGHT_GREEN if y == winner_year else CLUSTER_A for y in grouped["year"]]
    revenue_colors = [WINNER_GREEN       if y == winner_year else CLUSTER_B for y in grouped["year"]]

    fig = go.Figure()
    # Real data traces — showlegend=False; legend handled by dummy traces
    fig.add_trace(go.Bar(
        x            = grouped["year"].astype(str),
        y            = grouped["budget"],
        name         = "Budget",
        marker_color = budget_colors,
        offsetgroup  = 0,
        showlegend   = False,
    ))
    fig.add_trace(go.Bar(
        x            = grouped["year"].astype(str),
        y            = grouped["revenue"],
        name         = "Revenue",
        marker_color = revenue_colors,
        offsetgroup  = 1,
        showlegend   = False,
    ))

    # Dummy legend entries — blues first (others), greens second (winner)
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=CLUSTER_B,
                         name="Revenue (Other Years)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=CLUSTER_A,
                         name="Budget (Other Years)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=WINNER_GREEN,
                         name="Revenue — Highest Year (Winner)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=WINNER_LIGHT_GREEN,
                         name="Budget — Highest Year (Winner)", showlegend=True))

    fig.update_layout(
        barmode      = "group",
        title        = dict(
            text = "Average Budget vs Revenue per Year — Last 20 Years (Clustered Column Chart)",
            y    = 0.92,
            x    = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        xaxis_title  = "Release Year",
        yaxis_title  = "Average Amount (USD)",
        legend_title = "Financial Metric",
        # Legend anchored to bottom-right — safely below the title area
        legend       = dict(orientation="h", yanchor="bottom", y=1.01,
                            xanchor="center", x=0.5,
                            bordercolor="black", borderwidth=0.4,
                            font=dict(size=9),
                            itemwidth=30,
                            tracegroupgap=4),
        margin       = dict(t=110),   # extra top margin so legend sits between title and chart
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 2 — Clustered Bar Chart  (horizontal)
# Movie Output vs Revenue by Top Companies
# Color rule: CLUSTER_A for Output Count, CLUSTER_B for Revenue — no winner bar
# ─────────────────────────────────────────────
def output_revenue_clustered_bar(df):
    top_companies = df["main_company"].value_counts().head(10).index
    dff = df[df["main_company"].isin(top_companies)]

    grouped = dff.groupby("main_company").agg(
        output_count  = ("title",   "count"),
        total_revenue = ("revenue", "sum"),
    ).reset_index()

    # Winner = company with highest total revenue
    # Sort winner to the TOP of horizontal chart (last row = top in plotly h-bar)
    winner_company = grouped.loc[grouped["total_revenue"].idxmax(), "main_company"]
    winner_row     = grouped[grouped["main_company"] == winner_company]
    others         = grouped[grouped["main_company"] != winner_company].sort_values("total_revenue", ascending=True)
    grouped        = pd.concat([others, winner_row], ignore_index=True)  # winner last = topmost bar

    count_colors   = [WINNER_LIGHT_GREEN if c == winner_company else CLUSTER_A for c in grouped["main_company"]]
    revenue_colors = [WINNER_GREEN       if c == winner_company else CLUSTER_B for c in grouped["main_company"]]

    fig = go.Figure()
    # Real data traces — showlegend=False; legend handled by dummy traces
    fig.add_trace(go.Bar(
        y            = grouped["main_company"],
        x            = grouped["output_count"],
        name         = "Output Count",
        orientation  = "h",
        marker_color = count_colors,
        offsetgroup  = 0,
        showlegend   = False,
    ))
    fig.add_trace(go.Bar(
        y            = grouped["main_company"],
        x            = grouped["total_revenue"],
        name         = "Total Revenue",
        orientation  = "h",
        marker_color = revenue_colors,
        offsetgroup  = 1,
        showlegend   = False,
    ))

    # Dummy legend entries — blues first (others), greens second (winner)
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h", marker_color=CLUSTER_B,
                         name="Total Revenue (Other Companies)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h", marker_color=CLUSTER_A,
                         name="Output Count (Other Companies)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h", marker_color=WINNER_GREEN,
                         name="Revenue — Highest Company (Winner)", showlegend=True))
    fig.add_trace(go.Bar(x=[None], y=[None], orientation="h", marker_color=WINNER_LIGHT_GREEN,
                         name="Output Count — Highest Company (Winner)", showlegend=True))

    fig.update_layout(
        barmode      = "group",
        xaxis_type   = "log",
        title        = dict(
            text    = "Movie Output Count vs Total Revenue by Top Companies (Clustered Bar Chart)",
            y       = 0.98,
            x       = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        xaxis_title  = "Value (log scale)",
        yaxis_title  = "Production Company",
        legend_title = "Production Metric",
        # Legend placed at bottom to avoid title overlap
        legend       = dict(orientation="h", yanchor="bottom", y=1.01,
                            xanchor="center", x=0.5,
                            bordercolor="black", borderwidth=0.4,
                            font=dict(size=9),
                            itemwidth=30,
                            tracegroupgap=4),
        margin       = dict(t=120),   # extra top margin so legend sits between title and chart
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 3 — Scatter Chart
# Budget vs Box-Office Revenue
# ─────────────────────────────────────────────
def budget_revenue_scatter(df):
    fig = px.scatter(
        df,
        x         = "budget",
        y         = "revenue",
        opacity   = 0.55,
        trendline = "ols",
        title     = "Budget vs Box-Office Revenue (Scatter Chart)",
        labels    = {"budget": "Production Budget (USD)", "revenue": "Box-Office Revenue (USD)"},
        color_discrete_sequence = [BASE_BAR_COLOR],
    )
    fig.data[0].name       = "Movie"
    fig.data[0].showlegend = True
    if len(fig.data) > 1:
        fig.data[1].name       = "OLS Trendline"
        fig.data[1].showlegend = True

    fig.update_layout(
        legend_title = "Data Series",
        legend       = dict(orientation="h", yanchor="bottom", y=1.02,
                            xanchor="right", x=1,
                            bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 4 — Bubble Chart
# Budget vs Revenue with Popularity as bubble size
# ─────────────────────────────────────────────
def budget_revenue_bubble(df):
    fig = px.scatter(
        df.sample(min(1000, len(df)), random_state=1).head(100),  # Sample for performance
        x       = "budget",
        y       = "revenue",
        size    = "popularity",
        color   = "main_genre",
        opacity = 0.65,
        title   = "Budget vs Revenue — Bubble Size = Popularity (Bubble Chart)",
        labels  = {
            "budget":     "Production Budget (USD)",
            "revenue":    "Box-Office Revenue (USD)",
            "popularity": "Popularity Score",
            "main_genre": "Genre",
        },
        color_discrete_sequence = ACCENT_COLORS,
    )
    fig.update_layout(
        legend_title = "Genre",
        legend       = dict(orientation="v", yanchor="top", y=1,
                            xanchor="left", x=1.01,
                            title_font=dict(size=13)),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 8 — Line Chart
# Movie Output Over the Years
# ─────────────────────────────────────────────
def movie_output_over_years_line(df):
    dff = df.copy()
    dff["year"] = pd.to_datetime(dff["release_date"], errors="coerce").dt.year
    dff = dff.dropna(subset=["year"])
    grouped = dff.groupby("year").size().reset_index(name="movie_count")

    fig = px.line(
        grouped,
        x       = "year",
        y       = "movie_count",
        markers = True,
        title   = "Evolution of Movie Output Over Years (Line Chart)",
        labels  = {"year": "Release Year", "movie_count": "Number of Movies Produced"},
        color_discrete_sequence = ["#3B82F6"],
    )
    fig.data[0].name       = "Movies Produced"
    fig.data[0].showlegend = True

    fig.update_layout(
        legend_title = "Metric",
        legend       = dict(orientation="h", yanchor="bottom", y=1.02,
                            xanchor="right", x=1,
                            bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    return fig


# ─────────────────────────────────────────────
# WEEK 9 — Area Chart
# Total Industry Revenue Over Time
# ─────────────────────────────────────────────
def revenue_growth_area(df):
    dff = df.copy()
    dff["year"] = pd.to_datetime(dff["release_date"], errors="coerce").dt.year
    dff = dff.dropna(subset=["year"])
    grouped = dff.groupby("year")["revenue"].sum().reset_index()

    fig = px.area(
        grouped,
        x       = "year",
        y       = "revenue",
        title   = "Growth of Total Industry Revenue Over Time (Area Chart)",
        labels  = {"year": "Release Year", "revenue": "Total Revenue (USD)"},
        color_discrete_sequence = ["#22C55E"],
    )
    fig.data[0].name       = "Total Revenue"
    fig.data[0].showlegend = True

    fig.update_layout(
        legend_title = "Metric",
        legend       = dict(orientation="h", yanchor="bottom", y=1.02,
                            xanchor="right", x=1,
                            bordercolor="black", borderwidth=0.4),
        **LAYOUT_DEFAULTS
    )
    fig.update_traces(fillcolor="rgba(34,197,94,0.25)")
    return fig