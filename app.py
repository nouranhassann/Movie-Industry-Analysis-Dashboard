"""
app.py — Movie Industry Analysis Dashboard
TMDB 5000 Movie Dataset  |  Plotly Dash

Run:  python app.py
View: http://127.0.0.1:8050
"""

import pandas as pd
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import plotly.graph_objects as go

# ── Import all reusable chart functions from Charts.py ──────────────────────
from Charts import (
    # Week 1: Column + Bar
    genre_revenue_chart,
    runtime_by_company_chart,
    # Week 2: Stacked Column, Stacked Bar, Clustered Column, Clustered Bar
    stacked_revenue_chart,
    ratings_language_stacked_bar,
    budget_revenue_year_clustered_column,
    output_revenue_clustered_bar,
    # Week 3: Scatter
    budget_revenue_scatter,
    # Week 4: Bubble
    budget_revenue_bubble,
    # Week 8: Line
    movie_output_over_years_line,
    # Week 9: Area
    revenue_growth_area,
)

# ── Load dataset ─────────────────────────────────────────────────────────────
df = pd.read_csv("cleaned_data.csv")

LANGUAGE_MAP = {
    "en": "English",  "fr": "French",    "es": "Spanish",  "de": "German",
    "ja": "Japanese", "zh": "Chinese",   "ru": "Russian",  "it": "Italian",
    "ko": "Korean",   "hi": "Hindi",     "ar": "Arabic",   "pt": "Portuguese",
    "nl": "Dutch",    "sv": "Swedish",   "th": "Thai",     "cn": "Cantonese",
    "da": "Danish",   "tr": "Turkish",   "pl": "Polish",   "cs": "Czech",
    "ta": "Tamil",    "he": "Hebrew",    "fa": "Persian",  "vi": "Vietnamese",
    "xx": "No Language", "te": "Telugu", "ro": "Romanian",
}
if "original_language" in df.columns:
    df["original_language"] = df["original_language"].map(
        lambda x: LANGUAGE_MAP.get(x, str(x).upper())
    )

# ── Shared layout helpers ─────────────────────────────────────────────────────
CARD = {
    "backgroundColor": "#FFFFFF",
    "borderRadius":    "12px",
    "boxShadow":       "0 2px 12px rgba(0,0,0,0.10)",
    "padding":         "16px",
    "marginBottom":    "24px",
}
SECTION_HEADER = {
    "color":         "#1E3A5F",
    "fontFamily":    "Georgia, serif",
    "marginTop":     "36px",
    "marginBottom":  "8px",
    "borderBottom":  "3px solid #22C55E",
    "paddingBottom": "8px",
}
FILTER_BOX = {
    "flex":            "1",
    "backgroundColor": "#F8FAFC",
    "padding":         "16px",
    "borderRadius":    "10px",
    "border":          "1px solid #E2E8F0",
}

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Movie Industry Analysis Dashboard"

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(
    style={
        "padding":         "30px 40px",
        "backgroundColor": "#F0F4F8",
        "fontFamily":      "Georgia, serif",
        "maxWidth":        "1400px",
        "margin":          "0 auto",
    },
    children=[

        # ── Dashboard Header ─────────────────────────────────────────────────
        html.Div(
            style={
                "textAlign":       "center",
                "backgroundColor": "#1E3A5F",
                "borderRadius":    "14px",
                "padding":         "28px 16px",
                "marginBottom":    "36px",
                "boxShadow":       "0 4px 20px rgba(0,0,0,0.18)",
            },
            children=[
                html.H1(
                    " Movie Industry Analysis Dashboard",
                    style={"color": "#FFFFFF", "margin": "0 0 6px 0",
                           "fontFamily": "Georgia, serif", "fontSize": "2rem"}
                ),
                html.P(
                    "TMDB 5000 Movie Dataset  •  Financial · Genre · Distribution · Time-Series Analysis",
                    style={"color": "#94A3B8", "margin": 0, "fontSize": "14px"}
                ),
            ]
        ),

        # ════════════════════════════════════════════════════════════════════
        # SECTION 1 — COMPARISON CHARTS  (Week 1 & 2)
        # ════════════════════════════════════════════════════════════════════
        html.H2(" Comparison Charts", style=SECTION_HEADER),

        # Row: Column Chart + Bar Chart
        html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div(dcc.Graph(figure=genre_revenue_chart(df)),        style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(figure=runtime_by_company_chart(df)),   style={**CARD, "flex": "1"}),
        ]),

        # Row: Stacked Column + Stacked Bar
        html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div(dcc.Graph(figure=stacked_revenue_chart(df)),        style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(figure=ratings_language_stacked_bar(df)), style={**CARD, "flex": "1"}),
        ]),

        # Row: Clustered Column + Clustered Bar
        html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div(dcc.Graph(figure=budget_revenue_year_clustered_column(df)), style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(figure=output_revenue_clustered_bar(df)),         style={**CARD, "flex": "1"}),
        ]),

        # ════════════════════════════════════════════════════════════════════
        # SECTION 2 — RELATIONSHIP CHARTS  (Week 3 & 4)
        # ════════════════════════════════════════════════════════════════════
        html.H2(" Relationship Charts", style=SECTION_HEADER),

        html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div(dcc.Graph(figure=budget_revenue_scatter(df)), style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(figure=budget_revenue_bubble(df)),  style={**CARD, "flex": "1"}),
        ]),

        # ════════════════════════════════════════════════════════════════════
        # SECTION 3 — INTERACTIVE DISTRIBUTION CHARTS  (Week 5, 6, 7)
        # ════════════════════════════════════════════════════════════════════
        html.H2(" Distribution Charts — Interactive", style=SECTION_HEADER),

        html.P(
            "Use the controls below to filter by genre, rating range, and language. "
            "All three distribution charts update instantly.",
            style={"color": "#64748B", "marginBottom": "20px", "fontSize": "14px"},
        ),

        # ── Interactive Filters ──────────────────────────────────────────────
        html.Div(
            style={"display": "flex", "gap": "24px", "marginBottom": "24px", "alignItems": "flex-start"},
            children=[

                # Filter 1 — Genre
                html.Div(style=FILTER_BOX, children=[
                    html.Label("🎭 Filter by Genre",
                               style={"fontWeight": "bold", "color": "#1E3A5F",
                                      "marginBottom": "8px", "display": "block"}),
                    dcc.Dropdown(
                        id      = "genre-filter",
                        options = [{"label": g, "value": g}
                                   for g in sorted(df["main_genre"].dropna().unique())]
                                  if "main_genre" in df.columns else [],
                        value       = None,
                        placeholder = "All genres",
                        clearable   = True,
                        style       = {"color": "black"},
                    ),
                    html.Small("Select a genre to focus the distribution charts.",
                               style={"color": "#94A3B8", "marginTop": "6px",
                                      "display": "block", "fontSize": "11px"}),
                ]),

                # Filter 2 — Vote Average (slider + inputs)
                html.Div(style=FILTER_BOX, children=[
                    html.Label(" Filter by Vote Average",
                               style={"fontWeight": "bold", "color": "#1E3A5F",
                                      "marginBottom": "8px", "display": "block"}),
                    html.Div(style={"display": "flex", "gap": "8px", "marginBottom": "8px"}, children=[
                        dcc.Input(id="vote_average-min", type="number",
                                  min=0, max=10, step=0.1, value=0,
                                  style={"width": "48%", "borderRadius": "6px",
                                         "border": "1px solid #CBD5E1",
                                         "padding": "5px", "textAlign": "center"}),
                        dcc.Input(id="vote_average-max", type="number",
                                  min=0, max=10, step=0.1, value=10,
                                  style={"width": "48%", "borderRadius": "6px",
                                         "border": "1px solid #CBD5E1",
                                         "padding": "5px", "textAlign": "center"}),
                    ]),
                    dcc.RangeSlider(
                        id      = "vote_average-slider",
                        min=0, max=10, step=0.1, value=[0, 10],
                        marks   = {i: str(i) for i in range(0, 11, 2)},
                        tooltip = {"placement": "bottom", "always_visible": False},
                    ),
                    html.Small("Drag to isolate low- or high-rated movies.",
                               style={"color": "#94A3B8", "marginTop": "6px",
                                      "display": "block", "fontSize": "11px"}),
                ]),

                # Filter 3 — Language
                html.Div(style=FILTER_BOX, children=[
                    html.Label(" Filter by Language",
                               style={"fontWeight": "bold", "color": "#1E3A5F",
                                      "marginBottom": "8px", "display": "block"}),
                    dcc.Dropdown(
                        id      = "original_language-filter",
                        options = [{"label": l, "value": l}
                                   for l in sorted(df["original_language"].dropna().unique())]
                                  if "original_language" in df.columns else [],
                        value       = None,
                        placeholder = "All languages",
                        clearable   = True,
                        style       = {"color": "black"},
                    ),
                    html.Small("Pick a language to see its revenue profile.",
                               style={"color": "#94A3B8", "marginTop": "6px",
                                      "display": "block", "fontSize": "11px"}),
                ]),
            ]
        ),

        # ── Distribution Charts (dynamic) ───────────────────────────────────
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"},
            children=[
                html.Div(dcc.Graph(id="vote_average-histogram"), style={**CARD}),
                html.Div(dcc.Graph(id="runtime-boxplot"),        style={**CARD}),
                html.Div(dcc.Graph(id="revenue-violin"),
                         style={**CARD, "gridColumn": "1 / -1"}),
            ]
        ),

        # ════════════════════════════════════════════════════════════════════
        # SECTION 4 — TIME-SERIES CHARTS  (Week 8 & 9)
        # ════════════════════════════════════════════════════════════════════
        html.H2(" Time-Series Charts", style=SECTION_HEADER),

        html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div(dcc.Graph(figure=movie_output_over_years_line(df)), style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(figure=revenue_growth_area(df)),          style={**CARD, "flex": "1"}),
        ]),

        # ── Footer ───────────────────────────────────────────────────────────
        html.Div(
            "TMDB 5000 Movie Dataset  •  Plotly Dash Dashboard  •  Data Visualization Course",
            style={
                "textAlign":   "center",
                "color":       "#94A3B8",
                "fontSize":    "12px",
                "marginTop":   "40px",
                "paddingBottom": "20px",
            }
        ),
    ]
)


# ═══════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ═══════════════════════════════════════════════════════════════════════════

# ── Sync slider ↔ numeric inputs ─────────────────────────────────────────────
@app.callback(
    Output("vote_average-slider", "value"),
    Output("vote_average-min",    "value"),
    Output("vote_average-max",    "value"),
    Input("vote_average-slider",  "value"),
    Input("vote_average-min",     "value"),
    Input("vote_average-max",     "value"),
    prevent_initial_call=True,
)
def sync_slider_inputs(slider_val, min_val, max_val):
    trigger = ctx.triggered_id
    if trigger == "vote_average-slider":
        return slider_val, slider_val[0], slider_val[1]
    min_v = float(min_val) if min_val is not None else 0.0
    max_v = float(max_val) if max_val is not None else 10.0
    if min_v > max_v:
        min_v, max_v = max_v, min_v
    return [min_v, max_v], min_v, max_v


# ── Filter helper ─────────────────────────────────────────────────────────────
def _filter(df, genre, vote_range, language):
    dff = df.copy()
    lo, hi = vote_range
    dff = dff[(dff["vote_average"] >= lo) & (dff["vote_average"] <= hi)]
    if genre:
        dff = dff[dff["main_genre"] == genre]
    if language:
        dff = dff[dff["original_language"] == language]
    return dff


# ── Update distribution charts ────────────────────────────────────────────────
@app.callback(
    Output("vote_average-histogram", "figure"),
    Output("runtime-boxplot",        "figure"),
    Output("revenue-violin",         "figure"),
    Input("genre-filter",              "value"),
    Input("vote_average-slider",       "value"),
    Input("original_language-filter",  "value"),
)
def update_distribution_charts(genre, vote_range, language):
    LAYOUT = dict(
        template      = "plotly_white",
        title_x       = 0.5,
        title_font    = dict(size=15, family="Georgia, serif", color="black"),
        font          = dict(family="Georgia, serif", size=11, color="black"),
        paper_bgcolor = "white",
        plot_bgcolor  = "white",
    )
    filtered = _filter(df, genre, vote_range, language)

    # ── Week 5: Histogram ────────────────────────────────────────────────────
    fig_hist = px.histogram(
        filtered,
        x      = "vote_average",
        nbins  = 25,
        title  = "Vote Average Distribution (Histogram)",
        labels = {"vote_average": "Vote Average", "count": "Number of Movies"},
        color_discrete_sequence = ["#5B9BD5"],
    )
    fig_hist.data[0].name       = "Movie Count"
    fig_hist.data[0].showlegend = True
    fig_hist.update_layout(
        legend = dict(
            orientation = "h",
            yanchor     = "bottom", y=1.02,
            xanchor     = "right",  x=1,
            bgcolor     = "rgba(255,255,255,0.9)",
            bordercolor = "black",
            borderwidth = 1,
        ),
        **LAYOUT,
    )
    fig_hist.update_traces(marker_line_width=0.5, marker_line_color="white")

    # ── Week 6: Box Plot ─────────────────────────────────────────────────────
    box_data = filtered if genre else df
    fig_box = px.box(
        box_data,
        x      = "main_genre",
        y      = "runtime",
        color  = "main_genre",
        title  = "Runtime Distribution by Genre (Box Plot)",
        labels = {"main_genre": "Genre", "runtime": "Runtime (minutes)"},
        color_discrete_sequence = px.colors.qualitative.Set2,
    )
    fig_box.update_layout(
        showlegend   = True,
        legend_title = "Genre",
        legend       = dict(orientation="v", yanchor="top", y=1,
                            xanchor="left", x=1.01),
        **LAYOUT
    )

    # ── Week 7: Violin Plot ───────────────────────────────────────────────────
    violin_data = filtered if language else df
    top8        = violin_data["original_language"].value_counts().head(8).index
    violin_data = violin_data[violin_data["original_language"].isin(top8)]

    fig_violin = px.violin(
        violin_data,
        x      = "original_language",
        y      = "revenue",
        color  = "original_language",
        box    = True,
        points = "outliers",
        title  = "Revenue Distribution by Language (Violin Plot)",
        labels = {
            "original_language": "Language",
            "revenue":           "Box-Office Revenue (USD)",
        },
        color_discrete_sequence = px.colors.qualitative.Pastel,
    )
    fig_violin.update_layout(
        legend = dict(
            orientation = "h",
            yanchor     = "bottom", y=1.02,
            xanchor     = "right",  x=1,
            bgcolor     = "white",
            bordercolor = "black",
            borderwidth = 1,
        ),
        **LAYOUT,
    )

    return fig_hist, fig_box, fig_violin


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)