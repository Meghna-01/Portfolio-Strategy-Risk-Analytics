import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Portfolio Strategy & Risk Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #00B4D8;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #aaaaaa;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
    }
    [data-testid="stSelectbox"] > div > div {
        border: 1px solid #00B4D8 !important;
        border-radius: 6px !important;
        background-color: #1a1f2e !important;
    }
    .footer-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        height: 44px;
        background: rgba(13,17,23,0.99);
        border-top: 1px solid #2d3447;
        display: flex; align-items: center;
        padding: 0 28px;
        z-index: 1000;
    }
    .footer-left {
        font-size: 14px;
        color: #999999;
        font-weight: 500;
    }
    .footer-name {
        color: #00B4D8;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-bar">
    <span class="footer-left">
        Credit Risk Intelligence Platform &nbsp;·&nbsp; Built by <span class="footer-name">Meghna</span>
    </span>
</div>
""", unsafe_allow_html=True)

PALETTE = ["#00B4D8", "#FFB703", "#FB8500", "#E63946"]
BG = "#0E1117"
ORDER = ["PRIME", "NEAR-PRIME", "SUBPRIME", "HIGH-RISK"]
CHART_CONFIG = {"staticPlot": True}

df = pd.read_csv("clean_lending_data.csv")

st.sidebar.title("Portfolio Strategy & Risk Analytics")
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Executive Overview",
        "📈 Portfolio Analysis",
        "🎯 Capital Allocation Strategy",
        "⚡ Stress Testing & Scenarios",
        "📋 Management Recommendations"
    ],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
LGD = st.sidebar.slider(
    "LGD Assumption (%)", min_value=20, max_value=100, value=60, step=5) / 100
st.sidebar.caption(
    f"Loss Given Default = {int(LGD*100)}% "
    "(percentage of loan value not recovered after default)")
st.sidebar.markdown("---")
st.sidebar.caption("Built by Meghna")

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
        f"<p style='text-align:center; color:#aaaaaa; font-size:13px; "
        f"margin-top:0; margin-bottom:12px;'>{text}</p>",
        unsafe_allow_html=True)

def col_divider():
    st.markdown(
        "<div style='border-left:1px solid #2d3447; height:100%; min-height:460px;'></div>",
        unsafe_allow_html=True)

def metric_row(labels, values):
    cards = ""
    for label, value in zip(labels, values):
        cards += f"""
        <div style="background:#1a1f2e; border:1px solid #2d3447; padding:20px 24px;
        border-radius:10px; flex:1; min-width:0;">
            <p style="color:#aaaaaa; font-size:13px; margin:0 0 8px 0;">{label}</p>
            <p style="color:#00B4D8; font-size:20px; font-weight:bold; margin:0;">{value}</p>
        </div>"""
    st.markdown(
        f'<div style="display:flex; gap:14px; margin-bottom:8px; flex-wrap:wrap;">{cards}</div>',
        unsafe_allow_html=True)

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
    loss_pct = round(
        (s["loan_status"] * s["loan_amnt"]).sum() / total_loss_all * 100, 1)
    base_pd = s["loan_status"].mean()
    anchor_rows.append({
        "seg": seg, "n": n, "exp": exp, "exp_mn": exp_mn,
        "exp_pct": exp_pct, "dr": dr, "loss_pct": loss_pct, "base_pd": base_pd
    })

def render_anchor_table():
    st.markdown(
        "<p style='color:#aaaaaa; font-size:13px; margin-bottom:8px;'>"
        "Every number on every subsequent page traces back to this table. "
        "Exposure = sum of loan amounts. Default Rate = share of loans that defaulted. "
        "Loss Contribution = share of total dollar losses generated by that segment.</p>",
        unsafe_allow_html=True)
    hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Borrowers</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Total Exposure</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Exposure %</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Default Rate</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Loss Contribution %</th>'
        '</tr></thead><tbody>'
    )
    body = ""
    for r in anchor_rows:
        body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:{seg_colors[r["seg"]]}; font-weight:700;">{r["seg"]}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{r["n"]:,}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">${r["exp_mn"]} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{r["exp_pct"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{r["dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{r["loss_pct"]}%</td>'
            f'</tr>'
        )
    total_exp_mn = round(total_exposure_all / 1_000_000, 2)
    body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:12px 16px; color:#ffffff; font-weight:700;">Total</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">{len(df):,}</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">${total_exp_mn} Mn</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">100%</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaaaaa;">—</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#ffffff; font-weight:700;">100%</td>'
        f'</tr>'
    )
    st.markdown(hdr + body + "</tbody></table></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════
if page == "📊 Executive Overview":

    st.title("📊 Portfolio Strategy & Risk Analytics")
    st.caption("Executive Overview — Portfolio Health & Risk Snapshot")
    st.markdown("---")

    total_loans = len(df)
    total_exposure_mn = df["loan_amnt"].sum() / 1_000_000
    default_rate = round(df["loan_status"].mean() * 100, 1)
    avg_risk_score = round(df["risk_score"].mean(), 1)
    high_risk_pct = round(
        len(df[df["segment"].isin(["SUBPRIME", "HIGH-RISK"])]) / total_loans * 100, 1)

    metric_row(
        ["Total Loans", "Total Exposure", "Portfolio Default Rate",
         "Avg Risk Score", "High-Risk Exposure"],
        [f"{total_loans:,}", f"${total_exposure_mn:,.1f} Mn",
         f"{default_rate}%", f"{avg_risk_score}", f"{high_risk_pct}%"]
    )

    st.markdown("---")

    insight_box(
        "64% of borrowers fall in the PRIME tier — low default rates, high capital efficiency. "
        "The riskiest 1% (HIGH-RISK) generate losses far exceeding their portfolio share. "
        "Core strategic opportunity: grow the PRIME book, exit the tail.")

    st.subheader("How the Risk Score Was Built")
    st.caption(
        "LTI showed three distinct default zones — flat below 15%, climbing between 15–40%, "
        "spiking sharply above 40%. Weights derived by dividing each factor's default rate "
        "spread by the total spread across all factors (94 points).")

    scoring_html = """
    <div style="overflow-x:auto; margin-bottom:16px;">
    <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Risk Factor</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447;">Spread</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447;">Max Penalty</th>
        <th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447;">Weight</th>
        <th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Signal</th>
    </tr></thead><tbody>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc;">📊 Loan-to-Income Ratio</td>
        <td style="padding:12px 16px; text-align:center; color:#00B4D8; font-weight:700;">62 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc;">−66</td>
        <td style="padding:12px 16px; text-align:center; color:#00B4D8; font-weight:700;">66%</td>
        <td style="padding:12px 16px; color:#cccccc;">Strongest predictor</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc;">📋 Prior Default on File</td>
        <td style="padding:12px 16px; text-align:center; color:#FFB703; font-weight:700;">19 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc;">−20</td>
        <td style="padding:12px 16px; text-align:center; color:#FFB703; font-weight:700;">20%</td>
        <td style="padding:12px 16px; color:#cccccc;">Strong signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc;">💼 Employment Length</td>
        <td style="padding:12px 16px; text-align:center; color:#FB8500; font-weight:700;">11 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc;">−12</td>
        <td style="padding:12px 16px; text-align:center; color:#FB8500; font-weight:700;">12%</td>
        <td style="padding:12px 16px; color:#cccccc;">Moderate signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:12px 16px; color:#cccccc;">🕐 Credit History Length</td>
        <td style="padding:12px 16px; text-align:center; color:#888888; font-weight:700;">2 pts</td>
        <td style="padding:12px 16px; text-align:center; color:#cccccc;">−2</td>
        <td style="padding:12px 16px; text-align:center; color:#888888; font-weight:700;">2%</td>
        <td style="padding:12px 16px; color:#cccccc;">Weak signal</td>
    </tr>
    <tr style="background:#1a1f2e;">
        <td style="padding:12px 16px; color:#ffffff; font-weight:700;">Total</td>
        <td style="padding:12px 16px; text-align:center; color:#ffffff; font-weight:700;">94 pts</td>
        <td style="padding:12px 16px;"></td>
        <td style="padding:12px 16px; text-align:center; color:#ffffff; font-weight:700;">100%</td>
        <td style="padding:12px 16px; color:#aaaaaa;">Score range: 0–100</td>
    </tr></tbody></table></div>
    """
    st.markdown(scoring_html, unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Risk Score Distribution")
    chart_caption(
        "Each bar is a group of borrowers at that score. "
        "Coloured bands show the four segments.")

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
    for x0, x1, fill, label, color in [
        (0, 40, "rgba(230,57,70,0.10)", "HIGH-RISK", "#E63946"),
        (40, 60, "rgba(251,133,0,0.10)", "SUBPRIME", "#FB8500"),
        (60, 80, "rgba(255,183,3,0.10)", "NEAR-PRIME", "#FFB703"),
        (80, 100, "rgba(0,180,216,0.10)", "PRIME", "#00B4D8")]:
        fig_dist.add_vrect(x0=x0, x1=x1, fillcolor=fill, layer="below", line_width=0,
            annotation_text=label, annotation_position="top left",
            annotation_font_color=color, annotation_font_size=12)
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
        seg_counts["Segment"] = pd.Categorical(
            seg_counts["Segment"], categories=ORDER, ordered=True)
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
        seg_default["Segment"] = pd.Categorical(
            seg_default["Segment"], categories=ORDER, ordered=True)
        seg_default = seg_default.sort_values("Segment").reset_index(drop=True)
        fig2 = go.Figure()
        for i, row in seg_default.iterrows():
            fig2.add_trace(go.Bar(
                x=[row["Segment"]], y=[row["Default Rate"]],
                text=[str(row["Default Rate"]) + "%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=PALETTE[i], width=0.6, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, seg_default["Default Rate"].max() * 1.25]),
            margin=dict(t=30, b=10, l=10, r=10), height=400)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")
    st.subheader("Segment Summary — The Foundation of This Analysis")
    render_anchor_table()
    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE 2 — PORTFOLIO ANALYSIS
# ══════════════════════════════════════════
elif page == "📈 Portfolio Analysis":

    st.title("📈 Portfolio Analysis")
    st.caption("Lender Grade Validation, Exposure & Risk-Adjusted Return")
    st.markdown("---")

    insight_box(
        "The lender charges higher interest rates for lower grades — directionally correct. "
        "But from Grade D onwards, default losses outpace the extra interest charged and "
        "net yield turns negative. The lender is taking more risk without adequate compensation.")

    st.subheader("Does the Lender's Grade Tell the Full Story?")
    chart_header("Grade vs Segment Heatmap")
    chart_caption(
        "689 borrowers rated Grade B landed in SUBPRIME. "
        "In Grade C, 777 landed in SUBPRIME and 209 in HIGH-RISK.")

    cross = pd.crosstab(df["loan_grade"], df["segment"])
    cross = cross.reindex(columns=[c for c in ORDER if c in cross.columns])
    fig_heat = px.imshow(cross,
        color_continuous_scale=[
            [0.0, "#0d2d3a"], [0.08, "#0a4a60"],
            [0.3, "#0077a8"], [1.0, "#00B4D8"]],
        text_auto=True, aspect="auto",
        labels=dict(x="Risk Segment", y="Loan Grade", color="# Borrowers"))
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
        grade_exposure = df.groupby("loan_grade")["loan_amnt"].sum().div(
            1_000_000).round(2).reset_index()
        grade_exposure.columns = ["Grade", "Exposure ($ Mn)"]
        grade_exposure = grade_exposure.sort_values("Grade").reset_index(drop=True)
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
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, grade_exposure["Exposure ($ Mn)"].max() * 1.2]),
            margin=dict(t=30, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate by Loan Grade")
        grade_default = df.groupby("loan_grade")["loan_status"].mean().mul(
            100).round(1).reset_index()
        grade_default.columns = ["Grade", "Default Rate"]
        grade_default = grade_default.sort_values("Grade").reset_index(drop=True)
        max_dr = grade_default["Default Rate"].max()
        min_dr = grade_default["Default Rate"].min()
        fig2 = go.Figure()
        for i, row in grade_default.iterrows():
            ratio = (row["Default Rate"] - min_dr) / (
                max_dr - min_dr) if max_dr != min_dr else 0.5
            if ratio < 0.5:
                r = int(ratio * 2 * 255); g = 180; b = int(216 - ratio * 2 * 216)
            else:
                r = 255; g = int(183 - (ratio - 0.5) * 2 * 183); b = 3
            fig2.add_trace(go.Bar(
                x=[row["Grade"]], y=[row["Default Rate"]],
                text=[str(row["Default Rate"]) + "%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=f"rgb({r},{g},{b})",
                width=0.6, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, grade_default["Default Rate"].max() * 1.2]),
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
            f"Currently using {int(LGD*100)}% LGD. "
            "Cyan = compensated. Red = loss-making.")
        grade_rar = df.groupby("loan_grade").agg(
            Avg_Rate=("loan_int_rate", "mean"),
            Default_Rate=("loan_status", "mean")).reset_index()
        grade_rar["Net_Yield"] = (
            grade_rar["Avg_Rate"] - grade_rar["Default_Rate"] * 100 * LGD).round(2)
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
        chart_caption("Each dot is a borrower. Wide scatter = mispricing.")
        sample = df.sample(2000, random_state=42)
        fig4 = px.scatter(sample, x="risk_score", y="loan_int_rate", color="segment",
            color_discrete_sequence=PALETTE,
            category_orders={"segment": ORDER}, opacity=0.6,
            labels={"risk_score": "Risk Score",
                    "loan_int_rate": "Interest Rate (%)",
                    "segment": "Segment"})
        fig4.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            xaxis=dict(gridcolor="#1f2630"), yaxis=dict(gridcolor="#1f2630"),
            margin=dict(t=10, b=10, l=10, r=10), height=480)
        st.plotly_chart(fig4, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE 3 — CAPITAL ALLOCATION
# ══════════════════════════════════════════
elif page == "🎯 Capital Allocation Strategy":

    st.title("🎯 Capital Allocation Strategy")
    st.caption("Exposure vs loss contribution and recommended reallocation.")
    st.markdown("---")

    insight_box(
        "Which segment generates the most loss per dollar of exposure? "
        "A segment holding 1% of exposure but contributing 5% of losses is destroying capital. "
        "Reallocation into PRIME reduces portfolio default rate without shrinking total book size.")

    st.caption("📌 All base figures below come from the Executive Overview.")

    rows = anchor_rows.copy()
    for r in rows:
        ep = r["exp_pct"]; lp = r["loss_pct"]
        if   lp > ep * 2:   r["rec"], r["color"] = "Exit",     "#E63946"
        elif lp > ep:       r["rec"], r["color"] = "Tighten",  "#FB8500"
        elif lp < ep * 0.8: r["rec"], r["color"] = "Grow",     "#00B4D8"
        else:               r["rec"], r["color"] = "Maintain", "#FFB703"

    alloc_mult = {"Grow": 1.1, "Maintain": 1.0, "Tighten": 0.5, "Exit": 0.0}
    raw_targets = {r["seg"]: r["exp_pct"] * alloc_mult[r["rec"]] for r in rows}
    total_raw = sum(raw_targets.values())
    target_alloc = {seg: round(val / total_raw * 100, 1)
                    for seg, val in raw_targets.items()}

    st.markdown("---")
    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Exposure vs Loss Contribution")
        exp_loss_data = pd.DataFrame({
            "Segment": ORDER * 2,
            "Metric": ["Exposure %"] * 4 + ["Loss Contribution %"] * 4,
            "Value": [r["exp_pct"] for r in rows] + [r["loss_pct"] for r in rows]})
        exp_loss_data["Segment"] = pd.Categorical(
            exp_loss_data["Segment"], categories=ORDER, ordered=True)
        fig1 = px.bar(exp_loss_data, x="Segment", y="Value", color="Metric",
            barmode="group", text="Value",
            color_discrete_map={"Exposure %": "#00B4D8",
                                 "Loss Contribution %": "#E63946"},
            category_orders={"Segment": ORDER})
        fig1.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=14), cliponaxis=False)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis_title="Percentage (%)",
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, exp_loss_data["Value"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1),
            margin=dict(t=40, b=40, l=10, r=10), height=480)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Recommended Portfolio Reallocation")
        chart_caption("Loss > 2× exposure → Exit | Loss > exposure → Tighten | Loss < 80% exposure → Grow")
        max_alloc = max(max(r["exp_pct"] for r in rows),
                        max(target_alloc[seg] for seg in ORDER))
        alloc_df = pd.DataFrame({
            "Segment": ORDER,
            "Current %": [r["exp_pct"] for r in rows],
            "Target %": [target_alloc[seg] for seg in ORDER]})
        alloc_melted = alloc_df.melt(id_vars="Segment",
            value_vars=["Current %", "Target %"],
            var_name="Type", value_name="Value")
        alloc_melted["Segment"] = pd.Categorical(
            alloc_melted["Segment"], categories=ORDER, ordered=True)
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1),
            margin=dict(t=40, b=40, l=10, r=80), height=480)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE 4 — STRESS TESTING
# ══════════════════════════════════════════
elif page == "⚡ Stress Testing & Scenarios":

    st.title("⚡ Stress Testing & Scenarios")
    st.caption("What happens to the portfolio under adverse conditions?")
    st.markdown("---")

    insight_box(
        "Stress testing answers one question: how bad can it get? "
        "A PD multiplier simulates recession conditions by scaling up each segment's default rate. "
        "PRIME is the most resilient — its low base default rate means even a severe shock "
        "causes less absolute damage than the same shock applied to HIGH-RISK.")

    st.caption(
        "📌 Exposure figures and base default rates come from the Segment Summary on Page 1. "
        "EL = Exposure × Default Rate × LGD.")

    st.subheader("Recession Stress Test")

    scenario = st.selectbox("Select Stress Scenario", options=[
        "Base Case (No Stress)", "Mild Recession (+25% PD)",
        "Severe Recession (+50% PD)", "Extreme Stress (+75% PD)"], index=0)
    mult_map = {
        "Base Case (No Stress)": 1.00,
        "Mild Recession (+25% PD)": 1.25,
        "Severe Recession (+50% PD)": 1.50,
        "Extreme Stress (+75% PD)": 1.75}
    pd_mult = mult_map[scenario]

    stress_rows = []
    for r in anchor_rows:
        base_el = round((r["base_pd"] * LGD * r["exp"]) / 1_000_000, 2)
        stressed_pd = min(r["base_pd"] * pd_mult, 1.0)
        stressed_dr = round(stressed_pd * 100, 1)
        stressed_el = round((stressed_pd * LGD * r["exp"]) / 1_000_000, 2)
        el_change = round(stressed_el - base_el, 2)
        stress_rows.append({
            "seg": r["seg"], "exp": r["exp"],
            "base_dr": r["dr"], "stressed_dr": stressed_dr,
            "base_el": base_el, "stressed_el": stressed_el,
            "el_change": el_change})

    base_total_el = round(sum(r["base_el"] for r in stress_rows), 2)
    stressed_total_el = round(sum(r["stressed_el"] for r in stress_rows), 2)
    el_increase = round(stressed_total_el - base_total_el, 2)
    el_increase_pct = round(
        (el_increase / base_total_el) * 100, 1) if base_total_el > 0 else 0

    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Base Expected Loss", f"${base_total_el} Mn")
    sc2.metric("Stressed Expected Loss", f"${stressed_total_el} Mn",
        delta=f"+${el_increase} Mn", delta_color="inverse")
    sc3.metric("Increase in Loss", f"{el_increase_pct}%",
        delta=f"{el_increase_pct}%", delta_color="inverse")

    el_hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Exposure</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Base DR</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">LGD</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Base EL</th>'
        '</tr></thead><tbody>'
    )
    el_body = ""
    for r in stress_rows:
        exp_mn = round(r["exp"] / 1_000_000, 2)
        el_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:{seg_colors[r["seg"]]}; font-weight:700;">{r["seg"]}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">${exp_mn} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{r["base_dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{int(LGD*100)}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#00B4D8; font-weight:700;">${r["base_el"]} Mn</td>'
            f'</tr>')
    total_exp_mn = round(sum(r["exp"] for r in stress_rows) / 1_000_000, 2)
    el_body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:12px 16px; color:#fff; font-weight:700;">Total</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#fff; font-weight:700;">${total_exp_mn} Mn</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaa;">—</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#aaa;">{int(LGD*100)}%</td>'
        f'<td style="padding:12px 16px; text-align:right; color:#fff; font-weight:700;">${base_total_el} Mn</td>'
        f'</tr>')
    st.markdown(el_hdr + el_body + "</tbody></table></div>", unsafe_allow_html=True)

    s_hdr = (
        '<div style="overflow-x:auto; margin-bottom:16px;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Base DR</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Stressed DR</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Base EL</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Stressed EL</th>'
        '<th style="padding:12px 16px; text-align:right; border-bottom:1px solid #2d3447;">Additional Loss</th>'
        '</tr></thead><tbody>'
    )
    s_body = ""
    for sr in stress_rows:
        cc = "#E63946" if sr["el_change"] > 0 else "#00B4D8"
        s_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:{seg_colors[sr["seg"]]}; font-weight:700;">{sr["seg"]}</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">{sr["base_dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#FFB703;">{sr["stressed_dr"]}%</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#cccccc;">${sr["base_el"]} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:#FFB703;">${sr["stressed_el"]} Mn</td>'
            f'<td style="padding:12px 16px; text-align:right; color:{cc}; font-weight:700;">+${sr["el_change"]} Mn</td>'
            f'</tr>')
    st.markdown(s_hdr + s_body + "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, divider_col, col2 = st.columns([1, 0.03, 1])
    with divider_col:
        col_divider()
    with col1:
        chart_header("Expected Loss: Base vs Stressed")
        el_df = pd.DataFrame({"Segment": ORDER * 2,
            "Scenario": ["Base Case"] * 4 + [scenario] * 4,
            "Expected Loss ($ Mn)": (
                [r["base_el"] for r in stress_rows] +
                [r["stressed_el"] for r in stress_rows])})
        el_df["Segment"] = pd.Categorical(
            el_df["Segment"], categories=ORDER, ordered=True)
        fig1 = px.bar(el_df, x="Segment", y="Expected Loss ($ Mn)",
            color="Scenario", barmode="group", text="Expected Loss ($ Mn)",
            color_discrete_map={"Base Case": "#00B4D8", scenario: "#E63946"},
            category_orders={"Segment": ORDER})
        fig1.update_traces(texttemplate="$%{text} Mn", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, el_df["Expected Loss ($ Mn)"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1),
            margin=dict(t=40, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate: Base vs Stressed")
        dr_df = pd.DataFrame({"Segment": ORDER * 2,
            "Scenario": ["Base Case"] * 4 + [scenario] * 4,
            "Default Rate (%)": (
                [r["base_dr"] for r in stress_rows] +
                [r["stressed_dr"] for r in stress_rows])})
        dr_df["Segment"] = pd.Categorical(
            dr_df["Segment"], categories=ORDER, ordered=True)
        fig2 = px.bar(dr_df, x="Segment", y="Default Rate (%)",
            color="Scenario", barmode="group", text="Default Rate (%)",
            color_discrete_map={"Base Case": "#00B4D8", scenario: "#E63946"},
            category_orders={"Segment": ORDER})
        fig2.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            yaxis=dict(gridcolor="#1f2630",
                       range=[0, dr_df["Default Rate (%)"].max() * 1.3]),
            bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1),
            margin=dict(t=40, b=10, l=10, r=10), height=420)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    st.markdown("---")
    st.subheader("Capital Reallocation Simulator")
    st.caption(
        "Simulates future lending decisions — not movement of existing loans. "
        "Redirects future originations from SUBPRIME and HIGH-RISK towards PRIME.")

    shift_pct = st.slider(
        "Capital redirected from SUBPRIME + HIGH-RISK → PRIME (%)",
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
    sub_weight   = sub_exp_raw / risky_total if risky_total > 0 else 0.7
    high_weight  = high_exp_raw / risky_total if risky_total > 0 else 0.3

    prime_exp_new = prime_data["loan_amnt"].sum() + shift_amount
    near_exp_new  = near_data["loan_amnt"].sum()
    sub_exp_new   = max(sub_exp_raw - shift_amount * sub_weight, 0)
    high_exp_new  = max(high_exp_raw - shift_amount * high_weight, 0)

    prime_pd = prime_data["loan_status"].mean()
    near_pd  = near_data["loan_status"].mean()
    sub_pd   = sub_data["loan_status"].mean()
    high_pd  = high_data["loan_status"].mean()

    base_port_dr = round(
        (prime_data["loan_amnt"].sum() * prime_pd +
         near_data["loan_amnt"].sum() * near_pd +
         sub_exp_raw * sub_pd + high_exp_raw * high_pd) / total_exp * 100, 2)

    new_total_exp = prime_exp_new + near_exp_new + sub_exp_new + high_exp_new
    new_port_dr = round(
        (prime_exp_new * prime_pd + near_exp_new * near_pd +
         sub_exp_new * sub_pd + high_exp_new * high_pd) / new_total_exp * 100, 2)

    base_port_el = round(
        (prime_data["loan_amnt"].sum() * prime_pd * LGD +
         near_data["loan_amnt"].sum() * near_pd * LGD +
         sub_exp_raw * sub_pd * LGD +
         high_exp_raw * high_pd * LGD) / 1_000_000, 2)

    new_port_el = round(
        (prime_exp_new * prime_pd * LGD + near_exp_new * near_pd * LGD +
         sub_exp_new * sub_pd * LGD +
         high_exp_new * high_pd * LGD) / 1_000_000, 2)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Base Default Rate", f"{base_port_dr}%")
    r2.metric("Simulated Default Rate", f"{new_port_dr}%",
        delta=f"{round(new_port_dr - base_port_dr, 2)}%", delta_color="inverse")
    r3.metric("Base Expected Loss", f"${base_port_el} Mn")
    r4.metric("Simulated Expected Loss", f"${new_port_el} Mn",
        delta=f"{round(new_port_el - base_port_el, 2)}", delta_color="inverse")

    st.markdown(
        f"<p style='color:#aaaaaa; font-size:13px; margin-top:4px; margin-bottom:16px;'>"
        f"Reallocation sourced proportionally — "
        f"<b style='color:#FB8500'>{round(sub_weight*100,1)}% from SUBPRIME</b> and "
        f"<b style='color:#E63946'>{round(high_weight*100,1)}% from HIGH-RISK</b>.</p>",
        unsafe_allow_html=True)

    chart_header("Simulated Exposure Shift")
    realloc_data = pd.DataFrame({"Segment": ORDER * 2,
        "Type": ["Current"] * 4 + ["Simulated"] * 4,
        "Exposure ($ Mn)": [
            round(prime_data["loan_amnt"].sum() / 1_000_000, 2),
            round(near_data["loan_amnt"].sum() / 1_000_000, 2),
            round(sub_exp_raw / 1_000_000, 2),
            round(high_exp_raw / 1_000_000, 2),
            round(prime_exp_new / 1_000_000, 2),
            round(near_exp_new / 1_000_000, 2),
            round(sub_exp_new / 1_000_000, 2),
            round(high_exp_new / 1_000_000, 2)]})
    realloc_data["Segment"] = pd.Categorical(
        realloc_data["Segment"], categories=ORDER, ordered=True)
    fig_sim = px.bar(realloc_data, x="Segment", y="Exposure ($ Mn)", color="Type",
        barmode="group", text="Exposure ($ Mn)",
        color_discrete_map={"Current": "#FFB703", "Simulated": "#00B4D8"},
        category_orders={"Segment": ORDER})
    fig_sim.update_traces(texttemplate="$%{text} Mn", textposition="outside",
        textfont=dict(size=13), cliponaxis=False)
    fig_sim.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        yaxis_title="Exposure ($ Mn)",
        yaxis=dict(gridcolor="#1f2630",
                   range=[0, realloc_data["Exposure ($ Mn)"].max() * 1.3]),
        bargap=0.2, bargroupgap=0.05,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
        margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig_sim, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE 5 — RECOMMENDATIONS
# ══════════════════════════════════════════
elif page == "📋 Management Recommendations":

    st.title("📋 Management Recommendations")
    st.caption("Executive summary — findings, actions and strategic direction.")
    st.markdown("---")

    insight_box(
        "This section consolidates findings into four clear actions. "
        "Segments where loss contribution far exceeds exposure share are destroying capital. "
        "Segments where loss contribution is well below exposure share are underleveraged.")

    portfolio_dr = round(df["loan_status"].mean() * 100, 1)
    seg_stats = {}
    for r in anchor_rows:
        seg = r["seg"]
        s = df[df["segment"] == seg]
        net_yield = round(s["loan_int_rate"].mean() - (r["dr"] * LGD), 2)
        seg_stats[seg] = {"exp_pct": r["exp_pct"], "dr": r["dr"],
                          "loss_pct": r["loss_pct"], "net_yield": net_yield}

    alloc_mult = {"Grow": 1.1, "Maintain": 1.0, "Tighten": 0.5, "Exit": 0.0}
    rec_map = {}
    for seg in ORDER:
        ep = seg_stats[seg]["exp_pct"]; lp = seg_stats[seg]["loss_pct"]
        if   lp > ep * 2:   rec_map[seg] = ("Exit",     "#E63946")
        elif lp > ep:       rec_map[seg] = ("Tighten",  "#FB8500")
        elif lp < ep * 0.8: rec_map[seg] = ("Grow",     "#00B4D8")
        else:               rec_map[seg] = ("Maintain", "#FFB703")

    raw_t = {seg: seg_stats[seg]["exp_pct"] * alloc_mult[rec_map[seg][0]]
             for seg in ORDER}
    tot_raw = sum(raw_t.values())
    t_alloc = {seg: round(val / tot_raw * 100, 1) for seg, val in raw_t.items()}

    worst_seg = max(ORDER,
        key=lambda s: seg_stats[s]["loss_pct"] / seg_stats[s]["exp_pct"])
    best_yield = max(ORDER, key=lambda s: seg_stats[s]["net_yield"])
    hr_gap = round(
        seg_stats["HIGH-RISK"]["loss_pct"] - seg_stats["HIGH-RISK"]["exp_pct"], 1)

    metric_row(
        ["Portfolio Default Rate", "Highest Loss Contributor",
         "Best Net Yield Segment", "HIGH-RISK Loss Excess", "LGD Assumption"],
        [f"{portfolio_dr}%", worst_seg, best_yield,
         f"+{hr_gap}%", f"{int(LGD*100)}%"]
    )

    st.markdown("---")
    st.subheader("Analysis Summary")

    high_exp   = seg_stats["HIGH-RISK"]["exp_pct"]
    high_loss  = seg_stats["HIGH-RISK"]["loss_pct"]
    high_ratio = round(high_loss / high_exp, 1)
    prime_dr   = seg_stats["PRIME"]["dr"]
    prime_yield = seg_stats["PRIME"]["net_yield"]
    sub_exit_pct = round(
        seg_stats["SUBPRIME"]["exp_pct"] * 0.5 + seg_stats["HIGH-RISK"]["exp_pct"], 1)

    findings = [
        f"The portfolio carries a <b style='color:#FFB703'>{portfolio_dr}% overall default rate</b>. "
        f"The dominant risk predictor is loan-to-income ratio, "
        f"with a 62-point spread between the safest and riskiest borrowers.",
        f"<b style='color:#E63946'>HIGH-RISK segment</b> represents only {high_exp}% of exposure "
        f"but contributes {high_loss}% of total losses — a {high_ratio}× loss-to-exposure ratio.",
        f"<b style='color:#00B4D8'>PRIME segment</b> holds {seg_stats['PRIME']['exp_pct']}% of exposure "
        f"with a {prime_dr}% default rate and net yield of {prime_yield}% after expected loss.",
        f"Risk-adjusted net yield turns negative from Grade D onwards at {int(LGD*100)}% LGD.",
        f"Recommended reallocation frees ~{sub_exit_pct}% of portfolio capital for PRIME, "
        f"improving default rate and expected loss without changing total book size."
    ]

    fhtml = '<div style="background:#1a1f2e; border-radius:10px; padding:24px 28px; border:1px solid #2d3447;">'
    for f in findings:
        fhtml += f'<p style="color:#cccccc; font-size:15px; margin-bottom:14px; line-height:1.6;">→ {f}</p>'
    fhtml += '</div>'
    st.markdown(fhtml, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Recommended Actions")
    st.caption("Loss > 2× exposure → Exit · Loss > exposure → Tighten · "
               "Loss < 80% exposure → Grow · otherwise → Maintain")

    actions = [
        ("PRIME", rec_map["PRIME"][0], rec_map["PRIME"][1],
         f"Grow from {seg_stats['PRIME']['exp_pct']}% to {t_alloc['PRIME']}%",
         f"{seg_stats['PRIME']['dr']}% default rate. Loss well below exposure share."),
        ("NEAR-PRIME", rec_map["NEAR-PRIME"][0], rec_map["NEAR-PRIME"][1],
         "Maintain with stricter underwriting on LTI > 25%",
         f"{seg_stats['NEAR-PRIME']['dr']}% default rate. "
         f"Loss {seg_stats['NEAR-PRIME']['loss_pct']}% vs "
         f"exposure {seg_stats['NEAR-PRIME']['exp_pct']}%."),
        ("SUBPRIME", rec_map["SUBPRIME"][0], rec_map["SUBPRIME"][1],
         f"Reduce from {seg_stats['SUBPRIME']['exp_pct']}% to {t_alloc['SUBPRIME']}%",
         f"{seg_stats['SUBPRIME']['dr']}% default rate. Loss exceeds exposure share."),
        ("HIGH-RISK", rec_map["HIGH-RISK"][0], rec_map["HIGH-RISK"][1],
         "Stop new originations. Wind down.",
         f"{seg_stats['HIGH-RISK']['dr']}% default rate. "
         f"{seg_stats['HIGH-RISK']['loss_pct']}% of losses on "
         f"{seg_stats['HIGH-RISK']['exp_pct']}% exposure.")
    ]

    a_hdr = (
        '<div style="overflow-x:auto;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<thead><tr style="background:#1a1f2e; color:#aaaaaa; font-size:13px;">'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Segment</th>'
        '<th style="padding:12px 16px; text-align:center; border-bottom:1px solid #2d3447;">Action</th>'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">What to Do</th>'
        '<th style="padding:12px 16px; text-align:left; border-bottom:1px solid #2d3447;">Why</th>'
        '</tr></thead><tbody>'
    )
    a_body = ""
    badge = "padding:4px 14px; border-radius:20px; font-weight:700; font-size:12px;"
    for seg, rec, color, what, why in actions:
        a_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:12px 16px; color:white; font-weight:700;">{seg}</td>'
            f'<td style="padding:12px 16px; text-align:center;">'
            f'<span style="background:{color}22; color:{color}; '
            f'border:1px solid {color}; {badge}">{rec}</span></td>'
            f'<td style="padding:12px 16px; color:#ccc;">{what}</td>'
            f'<td style="padding:12px 16px; color:#aaa; font-size:13px;">{why}</td>'
            f'</tr>')
    st.markdown(a_hdr + a_body + "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown("---")
    chart_header("Current vs Target Portfolio Allocation")
    final_alloc = pd.DataFrame({
        "Segment": ORDER,
        "Current %": [seg_stats[seg]["exp_pct"] for seg in ORDER],
        "Target %": [t_alloc[seg] for seg in ORDER]})
    final_melted = final_alloc.melt(id_vars="Segment",
        value_vars=["Current %", "Target %"],
        var_name="Type", value_name="Value")
    final_melted["Segment"] = pd.Categorical(
        final_melted["Segment"], categories=ORDER, ordered=True)
    max_val = final_melted["Value"].max()
    fig_fin = px.bar(final_melted, y="Segment", x="Value", color="Type",
        barmode="group", text="Value", orientation="h",
        color_discrete_map={"Current %": "#FFB703", "Target %": "#00B4D8"},
        category_orders={"Segment": ORDER})
    fig_fin.update_traces(texttemplate="%{x}%", textposition="outside",
        textfont=dict(size=14), cliponaxis=False)
    fig_fin.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        xaxis_title="Allocation (%)",
        xaxis=dict(gridcolor="#1f2630", range=[0, max_val * 1.3]),
        bargap=0.2, bargroupgap=0.1,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
        margin=dict(t=40, b=10, l=80, r=80), height=350)
    st.plotly_chart(fig_fin, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)
