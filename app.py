"""
ESG Scoring Tool — Streamlit Dashboard
Author: Wilfried LAWSON HELLU | github.com/Wxlly00
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from esg_screener import ESGScorer, SUB_CRITERIA_LABELS

st.set_page_config(
    page_title="ESG Scoring Tool | Wilfried LAWSON HELLU",
    page_icon="🌱",
    layout="wide",
)

st.markdown("""
<style>
.main { background-color: #050D1A; }
h1, h2, h3 { font-family: Georgia, serif; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌱 ESG Tool")
    st.markdown("### Pillar Weights")
    e_w = st.slider("🌍 Environmental (%)", 0, 100, 40, step=5)
    s_w = st.slider("👥 Social (%)", 0, 100, 30, step=5)
    g_w = st.slider("🏛️ Governance (%)", 0, 100, 30, step=5)
    total_w = e_w + s_w + g_w
    if total_w != 100:
        st.warning(f"Weights sum to {total_w}% (must be 100%)")
        st.stop()

    st.markdown("### Screening")
    min_score = st.slider("Min ESG Score", 0, 100, 0, step=5)
    all_sectors = ["Industrial", "Food & Bev", "Consumer", "Chemical", "Healthcare",
                   "Luxury", "Finance", "Aerospace", "Energy", "Auto", "Pharma"]
    excluded_sectors = st.multiselect("Exclude Sectors", all_sectors, default=[])

    st.markdown("---")
    st.caption("By [Wilfried LAWSON HELLU](https://linkedin.com/in/wilfried-lawsonhellu)")

# ─── Initialize scorer ─────────────────────────────────────────────────────
scorer = ESGScorer(weights={"E": e_w/100, "S": s_w/100, "G": g_w/100})
scores = scorer.screen(min_score=min_score, excluded_sectors=excluded_sectors)
all_scores = scorer.pillar_scores()

# ─── Main ─────────────────────────────────────────────────────────────────
st.title("🌱 ESG Scoring & Screening Tool")
st.markdown(f"*Weights: E={e_w}% / S={s_w}% / G={g_w}% | Universe: {len(scores)} companies*")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Universe", "🔥 Heatmap", "🎯 Company Profile", "💼 Portfolio"])

# ─── Tab 1: Universe Overview ─────────────────────────────────────────────
with tab1:
    st.subheader("ESG Universe — Ranked Overview")

    # Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Companies", len(scores))
    c2.metric("Average ESG", f"{scores['ESG_Score'].mean():.1f}")
    c3.metric("Leaders (>75)", len(scores[scores["ESG_Score"] > 75]))
    c4.metric("Laggards (<50)", len(scores[scores["ESG_Score"] < 50]))

    # Color-coded table
    def color_score(val):
        if isinstance(val, str):
            return ""
        if val >= 75:
            return "background-color: rgba(76,175,80,0.15); color: #4CAF50"
        elif val >= 50:
            return "background-color: rgba(255,193,7,0.15); color: #FFC107"
        else:
            return "background-color: rgba(239,68,68,0.15); color: #EF4444"

    display = scores[["Rank", "Company", "Sector", "Country", "E_Score", "S_Score", "G_Score", "ESG_Score", "Classification"]].copy()
    display = display.rename(columns={"E_Score": "E", "S_Score": "S", "G_Score": "G", "ESG_Score": "ESG"})
    
    styled = display.style.applymap(color_score, subset=["E", "S", "G", "ESG"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Bar chart
    fig = px.bar(
        scores.sort_values("ESG_Score"),
        x="ESG_Score", y="Company",
        orientation="h",
        color="ESG_Score",
        color_continuous_scale=[[0, "#EF4444"], [0.5, "#FFC107"], [1, "#4CAF50"]],
        range_color=[30, 95],
        title="ESG Composite Scores — Full Universe",
        labels={"ESG_Score": "ESG Score", "Company": ""},
    )
    fig.update_layout(
        paper_bgcolor="#050D1A", plot_bgcolor="#050D1A",
        font_color="#94A3B8", title_font_color="white",
        height=500, coloraxis_showscale=False,
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)


# ─── Tab 2: Heatmap ───────────────────────────────────────────────────────
with tab2:
    st.subheader("ESG Sub-Criteria Heatmap")
    heatmap_df = scorer.heatmap_data()
    
    # Filter to screened companies
    heatmap_df = heatmap_df[heatmap_df.index.isin(scores["Company"])]

    fig = px.imshow(
        heatmap_df,
        color_continuous_scale=[[0, "#EF4444"], [0.4, "#FFC107"], [0.7, "#8BC34A"], [1, "#4CAF50"]],
        range_color=[30, 95],
        aspect="auto",
        title="ESG Sub-Criteria Scores (0–100)",
    )
    fig.update_layout(
        paper_bgcolor="#050D1A", plot_bgcolor="#050D1A",
        font_color="#94A3B8", title_font_color="white",
        xaxis=dict(tickangle=-35),
        height=550,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Green = Strong ESG performance | Red = Weak ESG performance")


# ─── Tab 3: Company Profile ───────────────────────────────────────────────
with tab3:
    st.subheader("Company Deep-Dive")
    company_list = scores["Company"].tolist()
    selected_company = st.selectbox("Select Company", company_list)

    if selected_company:
        profile = scorer.company_profile(selected_company)
        company_row = scores[scores["Company"] == selected_company].iloc[0]

        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ESG Score", f"{company_row['ESG_Score']:.1f}")
        m2.metric("E Score", f"{company_row['E_Score']:.1f}")
        m3.metric("S Score", f"{company_row['S_Score']:.1f}")
        m4.metric("G Score", f"{company_row['G_Score']:.1f}")

        # Radar chart
        labels = list(profile.keys())
        values = list(profile.values())
        values += [values[0]]
        labels += [labels[0]]

        fig = go.Figure(go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            fillcolor="rgba(76,175,80,0.15)",
            line=dict(color="#4CAF50", width=2),
            marker=dict(size=5, color="#4CAF50"),
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1E2D45", color="#94A3B8"),
                angularaxis=dict(gridcolor="#1E2D45", color="#94A3B8"),
                bgcolor="#050D1A",
            ),
            paper_bgcolor="#050D1A",
            font=dict(color="#94A3B8"),
            title=dict(text=f"{selected_company} — ESG Profile", font=dict(color="white")),
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Classification badge
        classification = company_row["Classification"]
        st.info(f"**Classification:** {classification} | **Rank:** #{company_row['Rank']} out of {len(all_scores)} companies")


# ─── Tab 4: Portfolio Builder ─────────────────────────────────────────────
with tab4:
    st.subheader("ESG Portfolio Builder")
    
    selected_companies = st.multiselect(
        "Select Companies",
        scores["Company"].tolist(),
        default=scores["Company"].tolist()[:5],
    )

    if len(selected_companies) < 2:
        st.warning("Select at least 2 companies")
    else:
        st.markdown("**Equal-weight portfolio assumed**")
        n = len(selected_companies)
        weights = [1/n] * n

        portfolio = scorer.portfolio_esg(selected_companies, weights)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Portfolio ESG", f"{portfolio['Total']:.1f}")
        c2.metric("vs Universe Avg", f"{portfolio['vs_Benchmark']:+.1f}", delta_color="normal")
        c3.metric("E Score", f"{portfolio['E_Score']:.1f}")
        c4.metric("S Score", f"{portfolio['S_Score']:.1f}")

        # Portfolio vs universe bar
        compare_df = pd.DataFrame({
            "Metric": ["Environmental", "Social", "Governance", "Total ESG"],
            "Portfolio": [portfolio["E_Score"], portfolio["S_Score"], portfolio["G_Score"], portfolio["Total"]],
            "Universe Avg": [
                all_scores["E_Score"].mean(),
                all_scores["S_Score"].mean(),
                all_scores["G_Score"].mean(),
                all_scores["ESG_Score"].mean(),
            ],
        })

        fig = px.bar(
            compare_df, x="Metric", y=["Portfolio", "Universe Avg"],
            barmode="group",
            color_discrete_map={"Portfolio": "#C9A84C", "Universe Avg": "#4A6FA5"},
            title="Portfolio vs Universe Average",
        )
        fig.update_layout(
            paper_bgcolor="#050D1A", plot_bgcolor="#050D1A",
            font_color="#94A3B8", title_font_color="white",
        )
        st.plotly_chart(fig, use_container_width=True)

st.caption("Built by **Wilfried LAWSON HELLU** | Finance Analyst | github.com/Wxlly00")
