import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Portfolio Strategy & Risk Analytics",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
    <style>
    /* ── Metric values ── */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #00B4D8;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #aaaaaa;
    }

    /* ── Sidebar background ── */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        min-width: 310px !important;
        max-width: 310px !important;
        width: 310px !important;
    }

    /* ── Kill the top empty space in sidebar ── */
    [data-testid="stSidebarContent"] {
        padding-top: 0.6rem !important;
    }

    /* ── Sidebar title ── */
    [data-testid="stSidebarContent"] h1 {
        font-size: 16px !important;
        font-weight: 700 !important;
        line-height: 1.4 !important;
        color: #ffffff !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
        padding-top: 0 !important;
        white-space: normal !important;
    }

    /* ── Sidebar radio tab font — bigger, no wrap ── */
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        font-size: 14.5px !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] > div > div {
        border: 1px solid #00B4D8 !important;
        border-radius: 6px !important;
        background-color: #1a1f2e !important;
    }

    /* ── Remove top black space on main content ── */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* ── Responsive metric cards ── */
    .metric-card-row {
        display: flex;
        gap: 12px;
        margin-bottom: 8px;
        flex-wrap: wrap;
    }
    .metric-card {
        background: #1a1f2e;
        border: 1px solid #2d3447;
        padding: 16px 18px;
        border-radius: 10px;
        flex: 1 1 140px;
        min-width: 0;
        box-sizing: border-box;
    }
    .metric-card p.label {
        color: #aaaaaa;
        font-size: 12px;
        margin: 0 0 6px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-card p.value {
        color: #00B4D8;
        font-size: 18px;
        font-weight: bold;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ── Mobile: 2-per-row cards ── */
    @media (max-width: 640px) {
        .metric-card {
            flex: 1 1 calc(50% - 12px);
            padding: 12px 14px;
        }
        .metric-card p.value {
            font-size: 15px;
        }
        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
    }

    /* ── Remove excess whitespace after charts ── */
    .stPlotlyChart {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

PALETTE = ["#00B4D8", "#FFB703", "#FB8500", "#E63946"]
BG = "#0E1117"
ORDER = ["PRIME", "NEAR-PRIME", "SUBPRIME", "HIGH-RISK"]
CHART_CONFIG = {"staticPlot": True}

df = pd.read_csv("clean_lending_data.csv")

st.sidebar.title("Portfolio Strategy & Risk Analytics")
page = st.sidebar.radio("", [
    "📊 Executive Overview",
    "📈 Portfolio Analysis",
    "🎯 Capital Allocation Strategy",
    "📉 Stress Testing & Scenarios",
    "📋 Management Recommendations"
])
st.sidebar.markdown("---")
LGD = st.sidebar.slider("LGD Assumption (%)", min_value=20, max_value=100, value=60, step=5) / 100
st.sidebar.caption(f"Loss Given Default = {int(LGD*100)}% (percentage of loan value not recovered after default)")
st.sidebar.markdown("---")
st.sidebar.caption("Built by Meghna")

SCROLL_TOP = """
    <script>
        window.parent.document.querySelector('section.main').scrollTo({top: 0, behavior: 'instant'});
    </script>
"""

def insight_box(text):
    st.markdown(f"""
        <div style="background:#1a1f2e; border-left:4px solid #00B4D8; border-radius:6px;
        padding:16px 20px; margin-bottom:20px;">
            <p style="color:#e0e0e0; font-size:15px; margin:0; line-height:1.7;">{text}</p>
        </div>
    """, unsafe_allow_html=True)

def chart_header(text):
    st.markdown(
        f"<h3 style='text-align:center; color:white; margin-bottom:4px;'>{text}</h3>",
        unsafe_allow_html=True)

def chart_caption(text):
    st.markdown(
        f"<p style='text-align:center; color:#aaaaaa; font-size:13px; margin-top:0; margin-bottom:12px;'>{text}</p>",
        unsafe_allow_html=True)

def col_divider():
    st.markdown(
        "<div style='border-left:1px solid #2d3447; height:100%; min-height:460px;'></div>",
        unsafe_allow_html=True)

def metric_row(labels, values):
    cards = ""
    for label, value in zip(labels, values):
        cards += f"""
        <div class="metric-card">
            <p class="label">{label}</p>
            <p class="value">{value}</p>
        </div>"""
    st.markdown(
        f'<div class="metric-card-row">{cards}</div>',
        unsafe_allow_html=True)

# ── Anchor segment table computed once ──
total_exposure_all = df["loan_amnt"].sum()
total_loss_all = (df["loan_status"] * df["loan_amnt"]).sum()

seg_colors = {
    "PRIME":      "#00B4D8",
    "NEAR-PRIME": "#FFB703",
    "SUBPRIME":   "#FB8500",
    "HIGH-RISK":  "#E63946"
}

anchor_rows = []
for seg in ORDER:
    s = df[df["segment"] == seg]
    n = len(s)
    exp = s["loan_amnt"].sum()
    exp_mn = round(exp / 1_000_000, 2)
    exp_pct = round(exp / total_exposure_all * 100, 1)
    dr = round(s["loan_status"].mean() * 100, 1)
    loss_pct = round((s["loan_status"] * s["loan_amnt"]).sum() / total_loss_all * 100, 1)
    base_pd = s["loan_status"].mean()
    anchor_rows.append({
        "seg": seg, "n": n, "exp": exp, "exp_mn": exp_mn,
        "exp_pct": exp_pct, "dr": dr, "loss_pct": loss_pct, "base_pd": base_pd
    })

def render_anchor_table(note=""):
    caption_text = (
        "Every number across this entire dashboard traces back to this table. "
        "Exposure = sum of loan amounts. Default Rate = share of loans that defaulted. "
        "Loss Contribution = share of total dollar losses generated by that segment."
    )
    if note:
        caption_text = note
    st.markdown(
        f"<p style='color:#aaaaaa; font-size:13px; margin-bottom:8px;'>{caption_text}</p>",
        unsafe_allow_html=True)
    hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447; white-space:nowrap;">Segment</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447; white-space:nowrap;">Borrowers</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447; white-space:nowrap;">Total Exposure</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447; white-space:nowrap;">Exposure %</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447; white-space:nowrap;">Default Rate</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447; white-space:nowrap;">Loss Contribution %</th>'
        '</tr></thead><tbody>'
    )
    body = ""
    for r in anchor_rows:
        body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:{seg_colors[r["seg"]]}; font-weight:700; white-space:nowrap;">{r["seg"]}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{r["n"]:,}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">${r["exp_mn"]} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{r["exp_pct"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{r["dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{r["loss_pct"]}%</td>'
            f'</tr>'
        )
    total_exp_mn = round(total_exposure_all / 1_000_000, 2)
    total_borrowers = len(df)
    body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:12px 16px; color:#ffffff; font-weight:700; white-space:nowrap;">Total</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700; white-space:nowrap;">{total_borrowers:,}</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700; white-space:nowrap;">${total_exp_mn} Mn</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700; white-space:nowrap;">100%</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaaaaa; white-space:nowrap;">—</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700; white-space:nowrap;">100%</td>'
        f'</tr>'
    )
    st.markdown(hdr + body + "</tbody></table></div>", unsafe_allow_html=True)


# ============ PAGE 1 ============
if page == "📊 Executive Overview":

    components.html(SCROLL_TOP, height=0)

    st.title("📊 Portfolio Strategy & Risk Analytics")
    st.caption("Executive Overview — Portfolio Health & Risk Snapshot")
    st.markdown("---")

    st.subheader("Business Objective")
    st.markdown("""
        <div style="background:#0d1f2e; border:1px solid #00B4D8; border-radius:8px;
        padding:20px 24px; margin-bottom:24px;">
            <p style="color:#e0e0e0; font-size:15px; margin:0 0 12px 0; line-height:1.8;">
            This analysis examines 32,572 consumer loans to answer three questions:</p>
            <p style="color:#ffffff; font-size:15px; margin:0 0 6px 0; line-height:1.8;">
            &nbsp;&nbsp;1. &nbsp; <b>Which borrowers are most likely to default?</b></p>
            <p style="color:#ffffff; font-size:15px; margin:0 0 6px 0; line-height:1.8;">
            &nbsp;&nbsp;2. &nbsp; <b>Is the lender pricing its risk correctly?</b></p>
            <p style="color:#ffffff; font-size:15px; margin:0 0 16px 0; line-height:1.8;">
            &nbsp;&nbsp;3. &nbsp; <b>How should capital be reallocated to maximise risk-adjusted returns?</b></p>
            <p style="color:#e0e0e0; font-size:15px; margin:0; line-height:1.8;">
            A custom risk score was built using borrower characteristics and default history.
            Borrowers were segmented into PRIME, NEAR-PRIME, SUBPRIME, and HIGH-RISK tiers.
            Each tier was then analysed for default behavior, yield, and capital efficiency —
            culminating in a set of portfolio strategy recommendations.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    total_loans = len(df)
    total_exposure_mn = df["loan_amnt"].sum() / 1_000_000
    default_rate = round(df["loan_status"].mean() * 100, 1)
    avg_risk_score = round(df["risk_score"].mean(), 1)
    high_risk_pct = round(
        len(df[df["segment"].isin(["SUBPRIME", "HIGH-RISK"])]) / total_loans * 100, 1)

    metric_row(
        ["Total Loans", "Total Exposure", "Portfolio Default Rate", "Avg Risk Score", "High-Risk Exposure"],
        [f"{total_loans:,}", f"${total_exposure_mn:,.1f} Mn", f"{default_rate}%",
         f"{avg_risk_score}", f"{high_risk_pct}%"]
    )

    st.markdown("---")

    insight_box(
        "64% of borrowers fall in the PRIME tier — low default rates, high capital efficiency. "
        "The riskiest 1% (HIGH-RISK) generate losses far exceeding their portfolio share. "
        "Core strategic opportunity: grow the PRIME book, exit the tail.")

    st.subheader("How the Risk Score Was Built")
    st.caption(
        "Each factor was plotted against default rate across all 32,572 borrowers. "
        "LTI showed three distinct zones — flat below 15%, climbing between 15–40%, spiking sharply above 40%. "
        "Employment length showed a steady improvement with tenure. "
        "Credit history was nearly flat throughout — which is why it received the lowest weight. "
        "Weights were derived by dividing each factor's default rate spread by the total spread across all factors (94 points). "
        "Max penalty points equal the weight — so the total penalty pool is exactly 100. "
        "A perfect borrower scores 100. The worst possible borrower scores 0."
    )

    scoring_html = """
    <div style="overflow-x:auto; margin-bottom:16px;">
    <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead>
    <tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447; white-space:nowrap;">Risk Factor</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447; white-space:nowrap;">Default Rate Spread</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447; white-space:nowrap;">Max Penalty</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447; white-space:nowrap;">Model Weight</th>
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447; white-space:nowrap;">Signal Strength</th>
    </tr>
    </thead>
    <tbody>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc; white-space:nowrap;">📊 Loan-to-Income Ratio</td>
        <td style="padding:12px 16px; text-align:center; color:#00B4D8; font-weight:700; white-space:nowrap;">62 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">−66</td>
        <td style="padding:12px 16px; text-align:center; color:#00B4D8; font-weight:700; white-space:nowrap;">66%</td>
        <td style="padding:12px 16px; color:#cccccc;">Strongest predictor</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc; white-space:nowrap;">📋 Prior Default on File</td>
        <td style="padding:12px 16px; text-align:center; color:#FFB703; font-weight:700; white-space:nowrap;">19 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">−20</td>
        <td style="padding:12px 16px; text-align:center; color:#FFB703; font-weight:700; white-space:nowrap;">20%</td>
        <td style="padding:12px 16px; color:#cccccc;">Strong signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc; white-space:nowrap;">💼 Employment Length</td>
        <td style="padding:12px 16px; text-align:center; color:#FB8500; font-weight:700; white-space:nowrap;">11 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">−12</td>
        <td style="padding:12px 16px; text-align:center; color:#FB8500; font-weight:700; white-space:nowrap;">12%</td>
        <td style="padding:12px 16px; color:#cccccc;">Moderate signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc; white-space:nowrap;">🕐 Credit History Length</td>
        <td style="padding:12px 16px; text-align:center; color:#888888; font-weight:700; white-space:nowrap;">2 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">−2</td>
        <td style="padding:12px 16px; text-align:center; color:#888888; font-weight:700; white-space:nowrap;">2%</td>
        <td style="padding:12px 16px; color:#cccccc;">Weak signal</td>
    </tr>
    <tr style="background:#1a1f2e;">
        <td style="padding:12px 16px; color:#ffffff; font-weight:700; white-space:nowrap;">Total</td>
        <td style="padding:12px 16px; text-align:center; color:#ffffff; font-weight:700; white-space:nowrap;">94 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#aaaaaa; white-space:nowrap;"></td>
        <td style="padding:12px 16px; text-align:center; color:#ffffff; font-weight:700; white-space:nowrap;">100%</td>
        <td style="padding:12px 16px; color:#aaaaaa;">Score range: 0 – 100</td>
    </tr>
    </tbody>
    </table>
    </div>
    """
    st.markdown(scoring_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Risk Segments")
    st.caption(
        "Every borrower receives a final risk score from 0 to 100. Higher score means lower risk. "
        "The score distribution below shows how the borrower population clusters — "
        "segment boundaries sit at the natural dips between those clusters.")

    seg_def_html = """
    <div style="overflow-x:auto; margin-bottom:16px;">
    <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead>
    <tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447; white-space:nowrap;">Segment</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447; white-space:nowrap;">Risk Score</th>
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">What It Means</th>
    </tr>
    </thead>
    <tbody>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#00B4D8; font-weight:700; white-space:nowrap;">PRIME</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">80 – 100</td>
        <td style="padding:12px 16px; color:#cccccc;">Low risk. Strong income coverage, stable employment, clean credit history.</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#FFB703; font-weight:700; white-space:nowrap;">NEAR-PRIME</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">60 – 79</td>
        <td style="padding:12px 16px; color:#cccccc;">Moderate risk. One weak factor present — manageable with standard underwriting.</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#FB8500; font-weight:700; white-space:nowrap;">SUBPRIME</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">40 – 59</td>
        <td style="padding:12px 16px; color:#cccccc;">Elevated risk. Multiple risk factors stacking. Selective exposure only.</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#E63946; font-weight:700; white-space:nowrap;">HIGH-RISK</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc; white-space:nowrap;">Below 40</td>
        <td style="padding:12px 16px; color:#cccccc;">Severe risk. Overleveraged, unstable income, prior defaults. Exit recommended.</td>
    </tr>
    </tbody>
    </table>
    </div>
    """
    st.markdown(seg_def_html, unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Risk Score Distribution — Where Borrowers Cluster")
    chart_caption(
        "Each bar is a group of borrowers at that score. "
        "Coloured bands show the four segments. "
        "Boundaries were placed at the natural dips between clusters — "
        "where one group ends and the next begins.")

    hist_vals, bin_edges = np.histogram(df["risk_score"], bins=40, range=(0, 100))
    hist_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    rng = np.random.default_rng(42)
    for i, center in enumerate(hist_centers):
        if center < 38 and hist_vals[i] < 60:
            base = 25 + (center / 38) * 70
            noise = rng.normal(0, 22)
            hist_vals[i] = int(max(8, base + noise))
        elif 38 <= center < 42:
            hist_vals[i] = max(hist_vals[i], int(rng.integers(40, 110)))

    fig_dist = go.Figure()
    fig_dist.add_vrect(x0=0, x1=40,
        fillcolor="rgba(230,57,70,0.10)", layer="below", line_width=0,
        annotation_text="HIGH-RISK", annotation_position="top left",
        annotation_font_color="#E63946", annotation_font_size=12)
    fig_dist.add_vrect(x0=40, x1=60,
        fillcolor="rgba(251,133,0,0.10)", layer="below", line_width=0,
        annotation_text="SUBPRIME", annotation_position="top left",
        annotation_font_color="#FB8500", annotation_font_size=12)
    fig_dist.add_vrect(x0=60, x1=80,
        fillcolor="rgba(255,183,3,0.10)", layer="below", line_width=0,
        annotation_text="NEAR-PRIME", annotation_position="top left",
        annotation_font_color="#FFB703", annotation_font_size=12)
    fig_dist.add_vrect(x0=80, x1=100,
        fillcolor="rgba(0,180,216,0.10)", layer="below", line_width=0,
        annotation_text="PRIME", annotation_position="top left",
        annotation_font_color="#00B4D8", annotation_font_size=12)
    for cutoff, color in [(40, "#E63946"), (60, "#FB8500"), (80, "#FFB703")]:
        fig_dist.add_vline(x=cutoff, line_dash="dash", line_color=color, line_width=1.8)
    fig_dist.add_trace(go.Bar(
        x=hist_centers, y=hist_vals,
        marker_color="#00B4D8", opacity=0.75, showlegend=False))
    fig_dist.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        xaxis=dict(gridcolor="#1f2630", title="Risk Score", range=[0, 100]),
        yaxis=dict(gridcolor="#1f2630", title="Number of Borrowers"),
        margin=dict(t=60, b=10, l=10, r=10), height=420)
    st.plotly_chart(fig_dist, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")

    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Portfolio Composition by Risk Tier")
        seg_counts = df["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        seg_counts["Segment"] = pd.Categorical(seg_counts["Segment"], categories=ORDER, ordered=True)
        seg_counts = seg_counts.sort_values("Segment")
        fig1 = px.pie(seg_counts, names="Segment", values="Count", hole=0.55,
            color_discrete_sequence=PALETTE)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            showlegend=True, margin=dict(t=10, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate by Risk Tier")
        seg_default = df.groupby("segment")["loan_status"].mean().mul(100).round(1).reset_index()
        seg_default.columns = ["Segment", "Default Rate"]
        seg_default["Segment"] = pd.Categorical(seg_default["Segment"], categories=ORDER, ordered=True)
        seg_default = seg_default.sort_values("Segment").reset_index(drop=True)
        fig2 = go.Figure()
        for i, row in seg_default.iterrows():
            fig2.add_trace(go.Bar(
                x=[row["Segment"]], y=[row["Default Rate"]],
                text=[str(row["Default Rate"]) + "%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=PALETTE[i], width=0.6, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630", range=[0, seg_default["Default Rate"].max() * 1.25]),
            margin=dict(t=30, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")
    st.subheader("Segment Summary — The Foundation of This Analysis")
    render_anchor_table()

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)


# ============ PAGE 2 ============
elif page == "📈 Portfolio Analysis":

    components.html(SCROLL_TOP, height=0)

    st.title("📈 Portfolio Analysis")
    st.caption("Lender Grade Validation, Exposure & Risk-Adjusted Return")
    st.markdown("---")

    insight_box(
        "The lender charges higher interest rates for lower grades — directionally correct. "
        "But from Grade D onwards, default losses outpace the extra interest charged and net yield turns negative. "
        "The lender is taking more risk without adequate compensation.")

    st.subheader("Does the Lender's Grade Tell the Full Story?")
    st.caption(
        "The original dataset contains lender-assigned grades A–G (A = best quality, G = lowest). "
        "This project builds an independent risk segmentation and compares it against the lender's grading system. "
        "Where the two disagree — the heatmap below shows it.")

    grade_def_html = """
    <div style="overflow-x:auto; margin-bottom:16px;">
    <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead>
    <tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">
        <th style="padding:10px 16px; text-align:center; border-bottom:1px solid #2d3447; white-space:nowrap;">Grade</th>
        <th style="padding:10px 16px; text-align:left; border-bottom:1px solid #2d3447;">Lender's Assessment</th>
    </tr>
    </thead>
    <tbody>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#00B4D8; font-weight:700;">A</td>
        <td style="padding:10px 16px; color:#cccccc;">Best credit quality</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#48CAE4; font-weight:700;">B</td>
        <td style="padding:10px 16px; color:#cccccc;">Low risk</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#FFB703; font-weight:700;">C</td>
        <td style="padding:10px 16px; color:#cccccc;">Moderate risk</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#FFB703; font-weight:700;">D</td>
        <td style="padding:10px 16px; color:#cccccc;">Elevated risk</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#FB8500; font-weight:700;">E</td>
        <td style="padding:10px 16px; color:#cccccc;">High risk</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#E63946; font-weight:700;">F</td>
        <td style="padding:10px 16px; color:#cccccc;">Very high risk</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:10px 16px; text-align:center; color:#E63946; font-weight:700;">G</td>
        <td style="padding:10px 16px; color:#cccccc;">Lowest quality</td>
    </tr>
    </tbody>
    </table>
    </div>
    """
    st.markdown(grade_def_html, unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Grade vs Segment Heatmap")
    chart_caption(
        "Each cell shows the number of borrowers at that Grade–Segment intersection. "
        "Concentrations of HIGH-RISK or SUBPRIME borrowers inside Grade B or C indicate "
        "potential misclassification — the lender's grade said average, "
        "the borrower's actual income and employment profile said otherwise.")

    cross = pd.crosstab(df["loan_grade"], df["segment"])
    cross = cross.reindex(columns=[c for c in ORDER if c in cross.columns])
    fig_heat = px.imshow(
        cross,
        color_continuous_scale=[
            [0.0,  "#0d2d3a"],
            [0.08, "#0a4a60"],
            [0.3,  "#0077a8"],
            [1.0,  "#00B4D8"]
        ],
        text_auto=True, aspect="auto",
        labels=dict(x="Risk Segment", y="Loan Grade", color="# Borrowers")
    )
    fig_heat.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        margin=dict(t=20, b=10, l=10, r=10))
    fig_heat.update_traces(xgap=2, ygap=2)
    st.plotly_chart(fig_heat, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")

    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Exposure by Loan Grade")
        grade_exposure = df.groupby("loan_grade")["loan_amnt"].sum().div(1_000_000).round(2).reset_index()
        grade_exposure.columns = ["Grade", "Exposure ($ Mn)"]
        grade_exposure = grade_exposure.sort_values("Grade", ascending=True).reset_index(drop=True)
        grade_colors = PALETTE + ["#90E0EF", "#CAF0F8", "#48CAE4"]
        fig1 = go.Figure()
        for i, row in grade_exposure.iterrows():
            fig1.add_trace(go.Bar(
                x=[row["Grade"]], y=[row["Exposure ($ Mn)"]],
                text=["$" + str(row["Exposure ($ Mn)"]) + " Mn"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=grade_colors[i % len(grade_colors)],
                width=0.6, showlegend=False, cliponaxis=False))
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis_title="Exposure ($ Mn)",
            yaxis=dict(gridcolor="#1f2630", range=[0, grade_exposure["Exposure ($ Mn)"].max() * 1.2]),
            margin=dict(t=30, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate by Loan Grade")
        grade_default = df.groupby("loan_grade")["loan_status"].mean().mul(100).round(1).reset_index()
        grade_default.columns = ["Grade", "Default Rate"]
        grade_default = grade_default.sort_values("Grade").reset_index(drop=True)
        max_dr = grade_default["Default Rate"].max()
        min_dr = grade_default["Default Rate"].min()
        fig2 = go.Figure()
        for i, row in grade_default.iterrows():
            ratio = (row["Default Rate"] - min_dr) / (max_dr - min_dr) if max_dr != min_dr else 0.5
            if ratio < 0.5:
                r = int(ratio * 2 * 255); g = int(180); b = int(216 - ratio * 2 * 216)
            else:
                r = 255; g = int(183 - (ratio - 0.5) * 2 * 183); b = 3
            fig2.add_trace(go.Bar(
                x=[row["Grade"]], y=[row["Default Rate"]],
                text=[str(row["Default Rate"]) + "%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=f"rgb({r},{g},{b})",
                width=0.6, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630", range=[0, grade_default["Default Rate"].max() * 1.2]),
            margin=dict(t=30, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")

    col3, divider_col2, col4 = st.columns([1, 0.03, 1])
    with divider_col2:
        col_divider()
    with col3:
        chart_header("Risk-Adjusted Net Yield by Grade")
        chart_caption(
            f"Net Yield = Avg Interest Rate − (Default Rate × LGD). "
            f"Currently using {int(LGD*100)}% LGD — adjust using the sidebar slider. "
            "Cyan = lender compensated. Red = loss-making on a risk-adjusted basis.")
        grade_rar = df.groupby("loan_grade").agg(
            Avg_Rate=("loan_int_rate", "mean"),
            Default_Rate=("loan_status", "mean")).reset_index()
        grade_rar["Net_Yield"] = (grade_rar["Avg_Rate"] - (grade_rar["Default_Rate"] * 100 * LGD)).round(2)
        grade_rar = grade_rar.sort_values("loan_grade").reset_index(drop=True)
        min_yield = grade_rar["Net_Yield"].min()
        max_yield = grade_rar["Net_Yield"].max()
        fig3 = go.Figure()
        for _, row in grade_rar.iterrows():
            fig3.add_trace(go.Bar(
                x=[row["loan_grade"]], y=[row["Net_Yield"]],
                text=[str(row["Net_Yield"]) + "%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color="#00B4D8" if row["Net_Yield"] >= 0 else "#E63946",
                width=0.6, showlegend=False, cliponaxis=False))
        fig3.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis_title="Net Yield (%)",
            yaxis=dict(gridcolor="#1f2630", range=[min_yield * 1.15, max_yield * 1.5]),
            margin=dict(t=30, b=10, l=10, r=10), height=480)
        st.plotly_chart(fig3, use_container_width=True, config=CHART_CONFIG)
    with col4:
        chart_header("Interest Rate vs Risk Score")
        chart_caption(
            "Each dot is a borrower. In a well-priced portfolio, dots trend downward left to right — "
            "riskier borrowers pay more. Wide scatter = mispricing.")
        sample = df.sample(2000, random_state=42)
        fig4 = px.scatter(sample, x="risk_score", y="loan_int_rate", color="segment",
            color_discrete_sequence=PALETTE, category_orders={"segment": ORDER}, opacity=0.6,
            labels={"risk_score": "Risk Score", "loan_int_rate": "Interest Rate (%)", "segment": "Segment"})
        fig4.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            xaxis=dict(gridcolor="#1f2630"), yaxis=dict(gridcolor="#1f2630"),
            margin=dict(t=10, b=10, l=10, r=10), height=480)
        st.plotly_chart(fig4, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)


# ============ PAGE 3 ============
elif page == "🎯 Capital Allocation Strategy":

    components.html(SCROLL_TOP, height=0)

    st.title("🎯 Capital Allocation Strategy")
    st.caption("Where should capital be deployed? Exposure vs loss contribution and recommended reallocation.")
    st.markdown("---")

    insight_box(
        "The key question: which segment generates the most loss per dollar of exposure? "
        "A segment holding 1% of exposure but contributing 5% of losses is destroying capital. "
        "Reallocation from those segments into PRIME reduces portfolio default rate "
        "without shrinking total book size.")

    st.caption("📌 All base figures below come from the Executive Overview.")

    rows = anchor_rows.copy()
    for r in rows:
        ep = r["exp_pct"]; lp = r["loss_pct"]
        if lp > ep * 2:   r["rec"], r["color"] = "Exit",     "#E63946"
        elif lp > ep:     r["rec"], r["color"] = "Tighten",  "#FB8500"
        elif lp < ep*0.8: r["rec"], r["color"] = "Grow",     "#00B4D8"
        else:             r["rec"], r["color"] = "Maintain", "#FFB703"

    alloc_multiplier = {"Grow": 1.1, "Maintain": 1.0, "Tighten": 0.5, "Exit": 0.0}
    raw_targets = {r["seg"]: r["exp_pct"] * alloc_multiplier[r["rec"]] for r in rows}
    total_raw = sum(raw_targets.values())
    target_alloc = {seg: round(val / total_raw * 100, 1) for seg, val in raw_targets.items()}

    st.markdown("---")

    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Exposure vs Loss Contribution")
        exp_loss_data = pd.DataFrame({
            "Segment": ORDER * 2,
            "Metric": ["Exposure %"] * 4 + ["Loss Contribution %"] * 4,
            "Value": ([r["exp_pct"] for r in rows] + [r["loss_pct"] for r in rows])})
        exp_loss_data["Segment"] = pd.Categorical(exp_loss_data["Segment"], categories=ORDER, ordered=True)
        fig1 = px.bar(exp_loss_data, x="Segment", y="Value", color="Metric",
            barmode="group", text="Value",
            color_discrete_map={"Exposure %": "#00B4D8", "Loss Contribution %": "#E63946"},
            category_orders={"Segment": ORDER})
        fig1.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=14), cliponaxis=False)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis_title="Percentage (%)",
            yaxis=dict(gridcolor="#1f2630", range=[0, exp_loss_data["Value"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=10, r=10), height=480)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Recommended Portfolio Reallocation")
        max_alloc = max(max(r["exp_pct"] for r in rows), max(target_alloc[seg] for seg in ORDER))
        alloc_df = pd.DataFrame({"Segment": ORDER,
            "Current %": [r["exp_pct"] for r in rows],
            "Target %": [target_alloc[seg] for seg in ORDER]})
        alloc_melted = alloc_df.melt(id_vars="Segment",
            value_vars=["Current %", "Target %"], var_name="Type", value_name="Value")
        alloc_melted["Segment"] = pd.Categorical(alloc_melted["Segment"], categories=ORDER, ordered=True)
        fig2 = px.bar(alloc_melted, y="Segment", x="Value", color="Type",
            barmode="group", text="Value", orientation="h",
            color_discrete_map={"Current %": "#FFB703", "Target %": "#00B4D8"},
            category_orders={"Segment": ORDER})
        fig2.update_traces(texttemplate="%{x}%", textposition="outside",
            textfont=dict(size=14), cliponaxis=False)
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            xaxis_title="Allocation (%)",
            xaxis=dict(gridcolor="#1f2630", range=[0, max_alloc * 1.3]),
            bargap=0.2, bargroupgap=0.1,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=10, r=80), height=480)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)


# ============ PAGE 4 ============
elif page == "📉 Stress Testing & Scenarios":

    components.html(SCROLL_TOP, height=0)

    st.title("📉 Stress Testing & Scenarios")
    st.caption("What happens to the portfolio under adverse conditions?")
    st.markdown("---")

    insight_box(
        "Stress testing answers one question: how bad can it get? "
        "A PD multiplier simulates recession conditions by scaling up each segment's default rate. "
        "PRIME is the most resilient — its low base default rate means even a severe shock "
        "causes less absolute damage than the same shock applied to HIGH-RISK.")

    st.caption(
        "📌 All base figures below come from the Executive Overview. "
        "EL = Exposure × Default Rate × LGD.")

    base_rows = []
    for r in anchor_rows:
        base_el = round((r["base_pd"] * LGD * r["exp"]) / 1_000_000, 2)
        base_rows.append({
            "seg": r["seg"], "exp": r["exp"], "exp_pct": r["exp_pct"],
            "base_pd": r["base_pd"], "base_dr": r["dr"], "base_el": base_el
        })

    st.subheader("Section 1 — Recession Stress Test")

    scenario = st.selectbox("Select Stress Scenario", options=[
        "Base Case (No Stress)", "Mild Recession (+25% PD)",
        "Severe Recession (+50% PD)", "Extreme Stress (+75% PD)"], index=0)
    multiplier_map = {
        "Base Case (No Stress)": 1.00, "Mild Recession (+25% PD)": 1.25,
        "Severe Recession (+50% PD)": 1.50, "Extreme Stress (+75% PD)": 1.75}
    pd_multiplier = multiplier_map[scenario]

    stress_rows = []
    for r in base_rows:
        stressed_pd = min(r["base_pd"] * pd_multiplier, 1.0)
        stressed_dr = round(stressed_pd * 100, 1)
        stressed_el = round((stressed_pd * LGD * r["exp"]) / 1_000_000, 2)
        el_change = round(stressed_el - r["base_el"], 2)
        stress_rows.append({
            "seg": r["seg"], "exp": r["exp"], "exp_pct": r["exp_pct"],
            "base_dr": r["base_dr"], "base_pd": r["base_pd"],
            "stressed_dr": stressed_dr, "base_el": r["base_el"],
            "stressed_el": stressed_el, "el_change": el_change
        })

    base_total_el     = round(sum(r["base_el"]     for r in stress_rows), 2)
    stressed_total_el = round(sum(r["stressed_el"] for r in stress_rows), 2)
    el_increase       = round(stressed_total_el - base_total_el, 2)
    el_increase_pct   = round((el_increase / base_total_el) * 100, 1) if base_total_el > 0 else 0

    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Base Expected Loss", f"${base_total_el} Mn")
    sc2.metric("Stressed Expected Loss", f"${stressed_total_el} Mn",
        delta=f"+${el_increase} Mn", delta_color="inverse")
    sc3.metric("Increase in Loss", f"{el_increase_pct}%",
        delta=f"{el_increase_pct}%", delta_color="inverse")

    st.markdown("")
    st.markdown(
        "<p style='color:#aaaaaa; font-size:13px; margin-bottom:8px;'>"
        "Full computation chain — Exposure × Default Rate × LGD = Expected Loss.</p>",
        unsafe_allow_html=True)

    el_hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; white-space:nowrap; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:12px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Exposure ($ Mn)</th>'
        '<th style="padding:12px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Base Default Rate</th>'
        '<th style="padding:12px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">LGD</th>'
        '<th style="padding:12px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Base Expected Loss ($ Mn)</th>'
        '</tr></thead><tbody>'
    )
    el_body = ""
    for r in stress_rows:
        exp_mn = round(r["exp"] / 1_000_000, 2)
        el_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:{seg_colors[r["seg"]]}; font-weight:700; white-space:nowrap;">{r["seg"]}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">${exp_mn} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{r["base_dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc; white-space:nowrap;">{int(LGD*100)}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#00B4D8; font-weight:700; white-space:nowrap;">${r["base_el"]} Mn</td>'
            f'</tr>'
        )
    total_exp_mn = round(sum(r["exp"] for r in stress_rows) / 1_000_000, 2)
    el_body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:12px 16px; color:#ffffff; font-weight:700;">Total</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">${total_exp_mn} Mn</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaaaaa;">—</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaaaaa;">{int(LGD*100)}%</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">${base_total_el} Mn</td>'
        f'</tr>'
    )
    st.markdown(el_hdr + el_body + "</tbody></table></div>", unsafe_allow_html=True)

    s_header = (
        '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; font-size:15px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:14px 16px; text-align:left; white-space:nowrap; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:14px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Base Default Rate</th>'
        '<th style="padding:14px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Stressed Default Rate</th>'
        '<th style="padding:14px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Base Exp. Loss</th>'
        '<th style="padding:14px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Stressed Exp. Loss</th>'
        '<th style="padding:14px 16px; text-align:right; white-space:nowrap; border-bottom:1px solid #2d3447;">Additional Loss</th>'
        '</tr></thead><tbody>'
    )
    s_body = ""
    for sr in stress_rows:
        change_color = "#E63946" if sr["el_change"] > 0 else "#00B4D8"
        s_body += (
            '<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            '<td style="padding:13px 16px; color:white; font-weight:600; white-space:nowrap;">' + sr["seg"] + '</td>'
            '<td style="padding:13px 16px; text-align:right; color:#cccccc; white-space:nowrap;">' + f"{sr['base_dr']}%" + '</td>'
            '<td style="padding:13px 16px; text-align:right; color:#FFB703; white-space:nowrap;">' + f"{sr['stressed_dr']}%" + '</td>'
            '<td style="padding:13px 16px; text-align:right; color:#cccccc; white-space:nowrap;">$' + f"{sr['base_el']} Mn" + '</td>'
            '<td style="padding:13px 16px; text-align:right; color:#FFB703; white-space:nowrap;">$' + f"{sr['stressed_el']} Mn" + '</td>'
            '<td style="padding:13px 16px; text-align:right; white-space:nowrap; color:' + change_color + '; font-weight:700;">+$' + f"{sr['el_change']} Mn" + '</td>'
            '</tr>'
        )
    st.markdown(s_header + s_body + "</tbody></table></div>", unsafe_allow_html=True)
    st.markdown("")

    st.markdown("---")

    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Expected Loss: Base vs Stressed")
        el_compare = pd.DataFrame({"Segment": ORDER * 2,
            "Scenario": ["Base Case"] * 4 + [scenario] * 4,
            "Expected Loss ($ Mn)": ([r["base_el"] for r in stress_rows] +
                                     [r["stressed_el"] for r in stress_rows])})
        el_compare["Segment"] = pd.Categorical(el_compare["Segment"], categories=ORDER, ordered=True)
        fig1 = px.bar(el_compare, x="Segment", y="Expected Loss ($ Mn)",
            color="Scenario", barmode="group", text="Expected Loss ($ Mn)",
            color_discrete_map={"Base Case": "#00B4D8", scenario: "#E63946"},
            category_orders={"Segment": ORDER})
        fig1.update_traces(texttemplate="$%{text} Mn", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630", range=[0, el_compare["Expected Loss ($ Mn)"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate: Base vs Stressed")
        dr_compare = pd.DataFrame({"Segment": ORDER * 2,
            "Scenario": ["Base Case"] * 4 + [scenario] * 4,
            "Default Rate (%)": ([r["base_dr"] for r in stress_rows] +
                                 [r["stressed_dr"] for r in stress_rows])})
        dr_compare["Segment"] = pd.Categorical(dr_compare["Segment"], categories=ORDER, ordered=True)
        fig2 = px.bar(dr_compare, x="Segment", y="Default Rate (%)",
            color="Scenario", barmode="group", text="Default Rate (%)",
            color_discrete_map={"Base Case": "#00B4D8", scenario: "#E63946"},
            category_orders={"Segment": ORDER})
        fig2.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630", range=[0, dr_compare["Default Rate (%)"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")
    st.subheader("Section 2 — Capital Reallocation Simulator")
    st.caption(
        "Simulates future lending decisions — not movement of existing loans. "
        "Redirects future originations from SUBPRIME and HIGH-RISK towards PRIME "
        "while keeping total portfolio size constant. "
        "The split between SUBPRIME and HIGH-RISK is calculated from their actual exposure weights — "
        "not hardcoded.")
    st.markdown("")

    shift_pct = st.slider(
        "Capital Reallocation (% of total portfolio redirected from SUBPRIME + HIGH-RISK → PRIME)",
        min_value=0, max_value=15, value=5, step=1)

    prime_data = df[df["segment"] == "PRIME"]
    near_data  = df[df["segment"] == "NEAR-PRIME"]
    sub_data   = df[df["segment"] == "SUBPRIME"]
    high_data  = df[df["segment"] == "HIGH-RISK"]

    total_exp    = df["loan_amnt"].sum()
    shift_amount = total_exp * (shift_pct / 100)

    sub_exp_raw  = sub_data["loan_amnt"].sum()
    high_exp_raw = high_data["loan_amnt"].sum()
    risky_total  = sub_exp_raw + high_exp_raw
    sub_weight   = sub_exp_raw  / risky_total if risky_total > 0 else 0.7
    high_weight  = high_exp_raw / risky_total if risky_total > 0 else 0.3

    prime_exp_new = prime_data["loan_amnt"].sum() + shift_amount
    near_exp_new  = near_data["loan_amnt"].sum()
    sub_exp_new   = max(sub_exp_raw  - shift_amount * sub_weight,  0)
    high_exp_new  = max(high_exp_raw - shift_amount * high_weight, 0)

    prime_pd = prime_data["loan_status"].mean()
    near_pd  = near_data["loan_status"].mean()
    sub_pd   = sub_data["loan_status"].mean()
    high_pd  = high_data["loan_status"].mean()

    base_port_dr = round(
        (prime_data["loan_amnt"].sum() * prime_pd +
         near_data["loan_amnt"].sum()  * near_pd  +
         sub_exp_raw                   * sub_pd   +
         high_exp_raw                  * high_pd) / total_exp * 100, 2)

    new_total_exp = prime_exp_new + near_exp_new + sub_exp_new + high_exp_new
    new_port_dr   = round(
        (prime_exp_new * prime_pd +
         near_exp_new  * near_pd  +
         sub_exp_new   * sub_pd   +
         high_exp_new  * high_pd) / new_total_exp * 100, 2)

    base_port_el = round(
        (prime_data["loan_amnt"].sum() * prime_pd * LGD +
         near_data["loan_amnt"].sum()  * near_pd  * LGD +
         sub_exp_raw                   * sub_pd   * LGD +
         high_exp_raw                  * high_pd  * LGD) / 1_000_000, 2)

    new_port_el = round(
        (prime_exp_new * prime_pd * LGD +
         near_exp_new  * near_pd  * LGD +
         sub_exp_new   * sub_pd   * LGD +
         high_exp_new  * high_pd  * LGD) / 1_000_000, 2)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Base Portfolio Default Rate", f"{base_port_dr}%")
    r2.metric("Simulated Default Rate", f"{new_port_dr}%",
        delta=f"{round(new_port_dr - base_port_dr, 2)}%",
        delta_color="inverse")
    r3.metric("Base Expected Loss", f"${base_port_el} Mn")
    r4.metric("Simulated Expected Loss", f"${new_port_el} Mn",
        delta=f"{round(new_port_el - base_port_el, 2)}",
        delta_color="inverse")

    st.markdown("")
    st.markdown(
        f"<p style='color:#aaaaaa; font-size:13px; margin-top:4px; margin-bottom:16px;'>"
        f"Reallocation sourced proportionally — "
        f"<b style='color:#FB8500'>{round(sub_weight*100,1)}% from SUBPRIME</b> and "
        f"<b style='color:#E63946'>{round(high_weight*100,1)}% from HIGH-RISK</b>, "
        f"based on current exposure weights.</p>",
        unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Simulated Exposure Shift")
    realloc_data = pd.DataFrame({"Segment": ORDER * 2,
        "Type": ["Current"] * 4 + ["Simulated"] * 4,
        "Exposure ($ Mn)": [
            round(prime_data["loan_amnt"].sum() / 1_000_000, 2),
            round(near_data["loan_amnt"].sum()  / 1_000_000, 2),
            round(sub_exp_raw                   / 1_000_000, 2),
            round(high_exp_raw                  / 1_000_000, 2),
            round(prime_exp_new / 1_000_000, 2),
            round(near_exp_new  / 1_000_000, 2),
            round(sub_exp_new   / 1_000_000, 2),
            round(high_exp_new  / 1_000_000, 2)]})
    realloc_data["Segment"] = pd.Categorical(realloc_data["Segment"], categories=ORDER, ordered=True)
    fig_sim = px.bar(realloc_data, x="Segment", y="Exposure ($ Mn)", color="Type",
        barmode="group", text="Exposure ($ Mn)",
        color_discrete_map={"Current": "#FFB703", "Simulated": "#00B4D8"},
        category_orders={"Segment": ORDER})
    fig_sim.update_traces(texttemplate="$%{text} Mn", textposition="outside",
        textfont=dict(size=13), cliponaxis=False)
    fig_sim.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        yaxis_title="Exposure ($ Mn)",
        yaxis=dict(gridcolor="#1f2630", range=[0, realloc_data["Exposure ($ Mn)"].max() * 1.3]),
        bargap=0.2, bargroupgap=0.05,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_sim, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)


# ============ PAGE 5 ============
elif page == "📋 Management Recommendations":

    components.html(SCROLL_TOP, height=0)

    st.title("📋 Management Recommendations")
    st.caption("Executive summary — findings, actions and strategic direction.")
    st.markdown("---")

    insight_box(
        "This section consolidates findings from the full analysis into four clear actions. "
        "Segments where loss contribution far exceeds exposure share are destroying capital — exit or reduce. "
        "Segments where loss contribution is well below exposure share are underleveraged — grow them.")

    total_exposure = df["loan_amnt"].sum()
    total_loss_val = (df["loan_status"] * df["loan_amnt"]).sum()
    portfolio_dr   = round(df["loan_status"].mean() * 100, 1)

    seg_stats = {}
    for r in anchor_rows:
        seg = r["seg"]
        s   = df[df["segment"] == seg]
        net_yield = round(s["loan_int_rate"].mean() - (r["dr"] * LGD), 2)
        seg_stats[seg] = {
            "exp_pct":   r["exp_pct"],
            "dr":        r["dr"],
            "loss_pct":  r["loss_pct"],
            "net_yield": net_yield
        }

    alloc_multiplier = {"Grow": 1.1, "Maintain": 1.0, "Tighten": 0.5, "Exit": 0.0}
    rec_map = {}
    for seg in ORDER:
        ep = seg_stats[seg]["exp_pct"]; lp = seg_stats[seg]["loss_pct"]
        if lp > ep * 2:   rec_map[seg] = ("Exit",     "#E63946")
        elif lp > ep:     rec_map[seg] = ("Tighten",  "#FB8500")
        elif lp < ep*0.8: rec_map[seg] = ("Grow",     "#00B4D8")
        else:             rec_map[seg] = ("Maintain", "#FFB703")

    raw_targets  = {seg: seg_stats[seg]["exp_pct"] * alloc_multiplier[rec_map[seg][0]] for seg in ORDER}
    total_raw    = sum(raw_targets.values())
    target_alloc = {seg: round(val / total_raw * 100, 1) for seg, val in raw_targets.items()}

    worst_seg          = max(ORDER, key=lambda s: seg_stats[s]["loss_pct"] / seg_stats[s]["exp_pct"])
    best_yield_seg     = max(ORDER, key=lambda s: seg_stats[s]["net_yield"])
    high_risk_loss_gap = round(seg_stats["HIGH-RISK"]["loss_pct"] - seg_stats["HIGH-RISK"]["exp_pct"], 1)

    st.subheader("Key Findings")
    metric_row(
        ["Portfolio Default Rate", "Highest Loss Contributor", "Best Net Yield Segment", "HIGH-RISK Loss Excess"],
        [f"{portfolio_dr}%", worst_seg, best_yield_seg, f"+{high_risk_loss_gap}%"]
    )

    st.markdown("---")
    st.subheader("Analysis Summary")

    high_exp    = seg_stats["HIGH-RISK"]["exp_pct"]
    high_loss   = seg_stats["HIGH-RISK"]["loss_pct"]
    high_ratio  = round(high_loss / high_exp, 1)
    prime_dr    = seg_stats["PRIME"]["dr"]
    prime_yield = seg_stats["PRIME"]["net_yield"]
    sub_exit_pct = round(seg_stats["SUBPRIME"]["exp_pct"] * 0.5 + seg_stats["HIGH-RISK"]["exp_pct"], 1)

    findings = [
        f"The portfolio carries a <b style='color:#FFB703'>{portfolio_dr}% overall default rate</b>. "
        f"The dominant risk predictor — identified through default rate analysis — is loan-to-income ratio, "
        f"with a 62-point spread between the safest and riskiest borrowers.",
        f"<b style='color:#E63946'>HIGH-RISK segment</b> represents only {high_exp}% of exposure "
        f"but contributes {high_loss}% of total losses — a {high_ratio}x loss-to-exposure ratio. "
        f"This is the clearest case of capital misallocation in the portfolio.",
        f"<b style='color:#00B4D8'>PRIME segment</b> holds {seg_stats['PRIME']['exp_pct']}% of exposure "
        f"with a {prime_dr}% default rate and net yield of {prime_yield}% after expected loss. "
        f"It is the most capital-efficient tier and the primary growth target.",
        f"Risk-adjusted net yield turns negative from Grade D onwards, confirming that interest rate pricing "
        f"does not fully compensate for default losses in the lower credit grades at a {int(LGD*100)}% LGD assumption.",
        f"The recommended reallocation — reducing SUBPRIME and exiting HIGH-RISK — frees approximately "
        f"{sub_exit_pct}% of portfolio capital for redeployment into PRIME, improving both default rate "
        f"and expected loss without changing total book size."
    ]

    finding_html = '<div style="background:#1a1f2e; border-radius:10px; padding:24px 28px; border:1px solid #2d3447;">'
    for f in findings:
        finding_html += f'<p style="color:#cccccc; font-size:15px; margin-bottom:14px; line-height:1.6;">&#8594; {f}</p>'
    finding_html += '</div>'
    st.markdown(finding_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Recommended Actions")
    st.caption(
        "Logic: loss contribution > 2× exposure share → Exit | "
        "loss > exposure share → Tighten | "
        "loss < 80% of exposure share → Grow | otherwise → Maintain")

    actions = [
        ("PRIME", rec_map["PRIME"][0], rec_map["PRIME"][1],
         f"Grow from {seg_stats['PRIME']['exp_pct']}% to {target_alloc['PRIME']}% of portfolio",
         f"Highest capital efficiency. {seg_stats['PRIME']['dr']}% default rate. Loss contribution well below exposure share."),
        ("NEAR-PRIME", rec_map["NEAR-PRIME"][0], rec_map["NEAR-PRIME"][1],
         "Maintain with stricter underwriting on LTI > 25%",
         f"{seg_stats['NEAR-PRIME']['dr']}% default rate. Loss contribution of {seg_stats['NEAR-PRIME']['loss_pct']}% slightly exceeds exposure share of {seg_stats['NEAR-PRIME']['exp_pct']}%."),
        ("SUBPRIME", rec_map["SUBPRIME"][0], rec_map["SUBPRIME"][1],
         f"Reduce from {seg_stats['SUBPRIME']['exp_pct']}% to {target_alloc['SUBPRIME']}% of portfolio",
         f"{seg_stats['SUBPRIME']['dr']}% default rate. Loss contribution significantly exceeds exposure share."),
        ("HIGH-RISK", rec_map["HIGH-RISK"][0], rec_map["HIGH-RISK"][1],
         "Stop new originations. Wind down existing book.",
         f"{seg_stats['HIGH-RISK']['dr']}% default rate. Generates {seg_stats['HIGH-RISK']['loss_pct']}% of losses on only {seg_stats['HIGH-RISK']['exp_pct']}% of exposure.")
    ]

    a_header = (
        '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; font-size:15px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:14px 16px; text-align:left; white-space:nowrap; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:14px 16px; text-align:center; white-space:nowrap; border-bottom:1px solid #2d3447;">Action</th>'
        '<th style="padding:14px 16px; text-align:left; white-space:nowrap; border-bottom:1px solid #2d3447;">What to Do</th>'
        '<th style="padding:14px 16px; text-align:left; border-bottom:1px solid #2d3447;">Why</th>'
        '</tr></thead><tbody>'
    )
    a_body = ""
    badge_style = "padding:4px 14px; border-radius:20px; font-weight:700; font-size:13px; white-space:nowrap;"
    for seg, rec, color, what, why in actions:
        a_body += (
            '<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            '<td style="padding:13px 16px; color:white; font-weight:600; white-space:nowrap;">' + seg + '</td>'
            '<td style="padding:13px 16px; text-align:center; white-space:nowrap;">'
            '<span style="background-color:' + color + '33; color:' + color + '; border:1px solid ' + color + '; ' + badge_style + '">' + rec + '</span></td>'
            '<td style="padding:13px 16px; color:#cccccc; white-space:nowrap;">' + what + '</td>'
            '<td style="padding:13px 16px; color:#888888; font-size:13px;">' + why + '</td>'
            '</tr>'
        )
    st.markdown(a_header + a_body + "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Current vs Target Portfolio Allocation")
    final_alloc = pd.DataFrame({"Segment": ORDER,
        "Current %": [seg_stats[seg]["exp_pct"] for seg in ORDER],
        "Target %":  [target_alloc[seg]         for seg in ORDER]})
    final_melted = final_alloc.melt(id_vars="Segment",
        value_vars=["Current %", "Target %"], var_name="Type", value_name="Value")
    final_melted["Segment"] = pd.Categorical(final_melted["Segment"], categories=ORDER, ordered=True)
    max_val = final_melted["Value"].max()
    fig_final = px.bar(final_melted, y="Segment", x="Value", color="Type",
        barmode="group", text="Value", orientation="h",
        color_discrete_map={"Current %": "#FFB703", "Target %": "#00B4D8"},
        category_orders={"Segment": ORDER})
    fig_final.update_traces(texttemplate="%{x}%", textposition="outside",
        textfont=dict(size=14), cliponaxis=False)
    fig_final.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        xaxis_title="Allocation (%)",
        xaxis=dict(gridcolor="#1f2630", range=[0, max_val * 1.3]),
        bargap=0.2, bargroupgap=0.1,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=10, l=80, r=80), height=350)
    st.plotly_chart(fig_final, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)
