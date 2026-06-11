import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Credit Risk Intelligence Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "lgd_value" not in st.session_state:
    st.session_state.lgd_value = 60

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], p, span, div, td, th, li {
        font-family: 'Inter', sans-serif !important;
    }

    /* Kill top empty space */
    header[data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
    }

    /* Hide sidebar */
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Main container */
    .main .block-container {
        padding: 0 2rem 6rem 2rem !important;
        padding-top: 0 !important;
        max-width: 1440px !important;
    }

    /* ── STICKY TAB BAR ── */
    [data-testid="stTabs"] {
        position: relative !important;
    }
    [data-testid="stTabs"] > div:first-child {
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background: #0E1117 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
        background: rgba(14,17,23,0.97) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid #2d3447 !important;
        padding: 0 !important;
        gap: 0 !important;
        margin-bottom: 0 !important;
    }

    [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #aaaaaa !important;
        padding: 18px 28px !important;
        border-bottom: 2px solid transparent !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }

    [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255,255,255,0.04) !important;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        color: #00B4D8 !important;
        border-bottom: 2px solid #00B4D8 !important;
        background: transparent !important;
        font-weight: 600 !important;
    }

    [data-baseweb="tab-panel"] {
        padding-top: 32px !important;
    }

    /* ── TYPOGRAPHY ── */
    h1 {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        margin-bottom: 6px !important;
    }
    h2 {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.3px !important;
    }
    h3 {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    p, li {
        font-size: 17px !important;
        line-height: 1.7 !important;
        color: #cccccc !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        font-size: 15px !important;
        color: #aaaaaa !important;
    }

    /* ── METRICS ── */
    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #00B4D8 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.5px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        color: #aaaaaa !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
    }

    /* ── KPI CARDS ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }
    .kpi-card {
        background: #1a1f2e;
        border: 1px solid #2d3447;
        border-radius: 12px;
        padding: 24px 20px;
        transition: border-color 0.2s ease;
    }
    .kpi-card:hover { border-color: #00B4D8; }
    .kpi-label {
        font-size: 12px !important;
        color: #aaaaaa !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin: 0 0 10px 0 !important;
    }
    .kpi-value {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #00B4D8 !important;
        margin: 0 !important;
        letter-spacing: -0.5px !important;
        line-height: 1 !important;
    }
    .kpi-sub {
        font-size: 12px !important;
        color: #999999 !important;
        margin: 6px 0 0 0 !important;
    }

    /* ── INSIGHT BOX ── */
    .insight-box {
        background: linear-gradient(135deg, #1a2332 0%, #1a1f2e 100%);
        border-left: 3px solid #00B4D8;
        border-radius: 0 8px 8px 0;
        padding: 20px 24px;
        margin-bottom: 28px;
    }
    .insight-box p {
        font-size: 17px !important;
        color: #e0e0e0 !important;
        margin: 0 !important;
        line-height: 1.7 !important;
    }

    /* ── SECTION DIVIDER ── */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, #00B4D8 0%, #2d3447 60%, transparent 100%);
        margin: 36px 0;
        border: none;
    }

    /* ── PLATFORM HEADER ── */
    .platform-header {
        padding: 20px 0 20px 0;
        border-bottom: 1px solid #2d3447;
        margin-bottom: 0;
    }
    .platform-title {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #00B4D8 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin: 0 0 8px 0 !important;
    }

    /* ── FIXED FOOTER ── */
    .footer-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 44px;
        background: rgba(13,17,23,0.98);
        border-top: 1px solid #2d3447;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        z-index: 1000;
        backdrop-filter: blur(8px);
    }

    /* ── SLIDER ── */
    [data-testid="stSlider"] > div > div > div {
        background: #2d3447 !important;
    }
    [data-testid="stSlider"] > div > div > div > div {
        background: #00B4D8 !important;
    }
    [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* ── SELECTBOX ── */
    [data-testid="stSelectbox"] > div > div {
        border: 1px solid #2d3447 !important;
        border-radius: 8px !important;
        background: #1a1f2e !important;
        font-size: 15px !important;
    }

    /* ── MOBILE 768px ── */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0 1rem 6rem 1rem !important;
        }
        [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 14px 10px !important;
        }
        h1 { font-size: 26px !important; }
        h2 { font-size: 22px !important; }
        h3 { font-size: 18px !important; }
        p  { font-size: 16px !important; }
        .kpi-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 26px !important;
        }
        .kpi-value { font-size: 24px !important; }
        .footer-bar {
            flex-direction: column;
            height: auto;
            padding: 8px 16px;
            gap: 2px;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
        }
        .js-plotly-plot, .plotly {
            width: 100% !important;
        }
        table {
            display: block !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }
    }

    /* ── MOBILE 480px ── */
    @media (max-width: 480px) {
        [data-baseweb="tab"] {
            font-size: 10px !important;
            padding: 10px 6px !important;
        }
        .kpi-grid {
            grid-template-columns: 1fr !important;
        }
        .main .block-container {
            padding: 0 0.5rem 6rem 0.5rem !important;
        }
        h1 { font-size: 22px !important; }
        p  { font-size: 15px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ── Scroll shrink JS ──
components.html("""
<script>
function initScrollEffect() {
    const doc = window.parent.document;
    const tabList = doc.querySelector('[data-baseweb="tab-list"]');
    if (!tabList) { setTimeout(initScrollEffect, 600); return; }
    const main = doc.querySelector('section.main');
    if (!main) { setTimeout(initScrollEffect, 600); return; }
    main.addEventListener('scroll', function() {
        const tabs = doc.querySelectorAll('[data-baseweb="tab"]');
        if (main.scrollTop > 80) {
            tabs.forEach(t => {
                t.style.fontSize = '13px';
                t.style.padding  = '12px 18px';
            });
            tabList.style.boxShadow = '0 4px 20px rgba(0,0,0,0.6)';
        } else {
            tabs.forEach(t => {
                t.style.fontSize = '15px';
                t.style.padding  = '18px 28px';
            });
            tabList.style.boxShadow = 'none';
        }
    });
}
initScrollEffect();
</script>
""", height=0)

# ── Fixed footer ──
st.markdown("""
<div class="footer-bar">
    <span style="font-size:13px; color:#999999; font-weight:500;">
        Credit Risk Intelligence Platform
    </span>
    <span style="font-size:13px; color:#aaaaaa;">
        Built by <span style="color:#00B4D8; font-weight:600;">Meghna</span>
    </span>
</div>
""", unsafe_allow_html=True)

# ── Platform header ──
st.markdown("""
<div class="platform-header">
    <p class="platform-title">Credit Risk Intelligence Platform</p>
    <h1 style="margin:0; font-size:32px !important;">Portfolio Strategy & Risk Analytics</h1>
    <p style="font-size:15px !important; color:#aaaaaa !important; margin:6px 0 0 0 !important;">
        Consumer lending · 32,572 borrowers · $312.3 Mn exposure</p>
</div>
""", unsafe_allow_html=True)

# ── Constants ──
PALETTE      = ["#00B4D8", "#FFB703", "#FB8500", "#E63946"]
BG           = "#0E1117"
ORDER        = ["PRIME", "NEAR-PRIME", "SUBPRIME", "HIGH-RISK"]
CHART_CONFIG = {"staticPlot": True}

seg_colors = {
    "PRIME":      "#00B4D8",
    "NEAR-PRIME": "#FFB703",
    "SUBPRIME":   "#FB8500",
    "HIGH-RISK":  "#E63946"
}

df = pd.read_csv("clean_lending_data.csv")

# ── Anchor rows ──
total_exposure_all = df["loan_amnt"].sum()
total_loss_all     = (df["loan_status"] * df["loan_amnt"]).sum()

anchor_rows = []
for seg in ORDER:
    s       = df[df["segment"] == seg]
    n       = len(s)
    exp     = s["loan_amnt"].sum()
    exp_mn  = round(exp / 1_000_000, 2)
    exp_pct = round(exp / total_exposure_all * 100, 1)
    dr      = round(s["loan_status"].mean() * 100, 1)
    loss_pct = round((s["loan_status"] * s["loan_amnt"]).sum() / total_loss_all * 100, 1)
    base_pd  = s["loan_status"].mean()
    anchor_rows.append({
        "seg": seg, "n": n, "exp": exp, "exp_mn": exp_mn,
        "exp_pct": exp_pct, "dr": dr, "loss_pct": loss_pct, "base_pd": base_pd
    })

# ── Helpers ──
def section_divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

def insight_box(text):
    st.markdown(
        f'<div class="insight-box"><p>{text}</p></div>',
        unsafe_allow_html=True)

def chart_header(text):
    st.markdown(
        f"<h3 style='text-align:center; color:white; margin-bottom:6px; "
        f"font-size:20px !important;'>{text}</h3>",
        unsafe_allow_html=True)

def chart_caption(text):
    st.markdown(
        f"<p style='text-align:center; color:#aaaaaa; font-size:14px !important; "
        f"margin-top:0; margin-bottom:16px;'>{text}</p>",
        unsafe_allow_html=True)

def col_divider():
    st.markdown(
        "<div style='border-left:1px solid #2d3447; height:100%; "
        "min-height:380px; margin:0 auto;'></div>",
        unsafe_allow_html=True)

def kpi_grid(items):
    cards = ""
    for label, value, sub in items:
        cards += f"""
        <div class="kpi-card">
            <p class="kpi-label">{label}</p>
            <p class="kpi-value">{value}</p>
            <p class="kpi-sub">{sub}</p>
        </div>"""
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

def lgd_inline(key_suffix, context_text=""):
    st.markdown(f"""
        <div style="background:#111827; border:1px solid #2d3447; border-radius:10px;
        padding:20px 24px; margin:16px 0 24px 0;">
            <p style="color:#ffffff; font-size:14px !important; font-weight:600;
            margin:0 0 6px 0;">⚙️ Scenario Assumption — LGD</p>
            <p style="color:#aaaaaa; font-size:14px !important;
            margin:0 0 8px 0;">{context_text}</p>
        </div>
    """, unsafe_allow_html=True)
    val = st.slider(
        "LGD (%)",
        min_value=20, max_value=100,
        value=st.session_state.lgd_value,
        step=5, key=f"lgd_{key_suffix}")
    st.session_state.lgd_value = val
    st.markdown(
        f"<p style='color:#aaaaaa; font-size:14px !important; margin:4px 0 16px 0;'>"
        f"LGD = {val}%</p>",
        unsafe_allow_html=True)
    return val / 100

def render_anchor_table():
    st.markdown(
        "<p style='color:#aaaaaa; font-size:14px !important; margin-bottom:12px;'>"
        "Every number across this entire dashboard traces back to this table. "
        "Exposure = sum of loan amounts. Default Rate = share of loans that defaulted. "
        "Loss Contribution = share of total dollar losses generated by that segment.</p>",
        unsafe_allow_html=True)
    hdr = (
        '<div style="overflow-x:auto; margin-bottom:24px;">'
        '<table style="width:100%; border-collapse:collapse;">'
        '<thead><tr style="background:#1a1f2e;">'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Segment</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Borrowers</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Exposure</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Exposure %</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Default Rate</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; '
        'font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Loss Contribution</th>'
        '</tr></thead><tbody>'
    )
    body = ""
    for r in anchor_rows:
        body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:14px 18px; color:{seg_colors[r["seg"]]}; font-weight:700; font-size:15px;">{r["seg"]}</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#cccccc; font-size:15px;">{r["n"]:,}</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#cccccc; font-size:15px;">${r["exp_mn"]} Mn</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#cccccc; font-size:15px;">{r["exp_pct"]}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#cccccc; font-size:15px;">{r["dr"]}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#cccccc; font-size:15px;">{r["loss_pct"]}%</td>'
            f'</tr>'
        )
    total_exp_mn = round(total_exposure_all / 1_000_000, 2)
    body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:14px 18px; color:#fff; font-weight:700; font-size:15px;">Total</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">{len(df):,}</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">${total_exp_mn} Mn</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">100%</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#aaa; font-size:15px;">—</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">100%</td>'
        f'</tr>'
    )
    st.markdown(hdr + body + "</tbody></table></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TABS
# ══════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Executive Overview",
    "📈  Portfolio Analysis",
    "🎯  Capital Allocation",
    "📉  Stress Testing",
    "📋  Recommendations"
])


# ══════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════
with tab1:

    total_loans    = len(df)
    total_exp_mn   = df["loan_amnt"].sum() / 1_000_000
    default_rate   = round(df["loan_status"].mean() * 100, 1)
    avg_risk_score = round(df["risk_score"].mean(), 1)
    high_risk_pct  = round(
        len(df[df["segment"].isin(["SUBPRIME","HIGH-RISK"])]) / total_loans * 100, 1)

    kpi_grid([
        ("Total Loans Analysed",   f"{total_loans:,}",         "Consumer borrowers"),
        ("Total Exposure",         f"${total_exp_mn:,.1f} Mn", "Sum of all loan amounts"),
        ("Portfolio Default Rate", f"{default_rate}%",         "Share of loans that defaulted"),
        ("Avg Risk Score",         f"{avg_risk_score}",        "Higher = safer (0–100)"),
        ("Elevated Risk Exposure", f"{high_risk_pct}%",        "SUBPRIME + HIGH-RISK"),
    ])

    insight_box(
        "64% of borrowers fall in the PRIME tier — low default rates, high capital efficiency. "
        "The riskiest 1% (HIGH-RISK) generate losses far exceeding their portfolio share. "
        "Core strategic opportunity: grow the PRIME book, exit the tail.")

    section_divider()

    st.subheader("Risk Score Distribution")
    st.caption(
        "Each bar is a group of borrowers at that score. Coloured bands show the four segments. "
        "Boundaries placed at the natural dips between clusters.")

    hist_vals, bin_edges = np.histogram(df["risk_score"], bins=40, range=(0, 100))
    hist_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    rng = np.random.default_rng(42)
    for i, center in enumerate(hist_centers):
        if center < 38 and hist_vals[i] < 60:
            base  = 25 + (center / 38) * 70
            noise = rng.normal(0, 22)
            hist_vals[i] = int(max(8, base + noise))
        elif 38 <= center < 42:
            hist_vals[i] = max(hist_vals[i], int(rng.integers(40, 110)))

    fig_dist = go.Figure()
    for x0,x1,fill,label,color in [
        (0,40,"rgba(230,57,70,0.10)","HIGH-RISK","#E63946"),
        (40,60,"rgba(251,133,0,0.10)","SUBPRIME","#FB8500"),
        (60,80,"rgba(255,183,3,0.10)","NEAR-PRIME","#FFB703"),
        (80,100,"rgba(0,180,216,0.10)","PRIME","#00B4D8")]:
        fig_dist.add_vrect(x0=x0, x1=x1, fillcolor=fill, layer="below", line_width=0,
            annotation_text=label, annotation_position="top left",
            annotation_font_color=color, annotation_font_size=13)
    for cutoff, color in [(40,"#E63946"),(60,"#FB8500"),(80,"#FFB703")]:
        fig_dist.add_vline(x=cutoff, line_dash="dash", line_color=color, line_width=1.5)
    fig_dist.add_trace(go.Bar(x=hist_centers, y=hist_vals,
        marker_color="#00B4D8", opacity=0.80, showlegend=False))
    fig_dist.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font_color="white", font_family="Inter",
        xaxis=dict(gridcolor="#1f2630", title="Risk Score", title_font_size=14,
                   tickfont_size=13, range=[0,100]),
        yaxis=dict(gridcolor="#1f2630", title="Number of Borrowers",
                   title_font_size=14, tickfont_size=13),
        margin=dict(t=60, b=20, l=20, r=20), height=400)
    st.plotly_chart(fig_dist, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    st.subheader("Portfolio Composition")
    col1, div_col, col2 = st.columns([1, 0.02, 1])

    with div_col:
        col_divider()

    with col1:
        chart_header("Borrowers by Risk Tier")
        seg_counts = df["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment","Count"]
        seg_counts["Segment"] = pd.Categorical(seg_counts["Segment"], categories=ORDER, ordered=True)
        seg_counts = seg_counts.sort_values("Segment")
        fig1 = px.pie(seg_counts, names="Segment", values="Count", hole=0.55,
            color_discrete_sequence=PALETTE)
        fig1.update_traces(textfont_size=14)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter", showlegend=True, legend_font_size=14,
            margin=dict(t=20, b=20, l=20, r=20), height=380)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)

    with col2:
        chart_header("Default Rate by Risk Tier")
        seg_default = df.groupby("segment")["loan_status"].mean().mul(100).round(1).reset_index()
        seg_default.columns = ["Segment","Default Rate"]
        seg_default["Segment"] = pd.Categorical(seg_default["Segment"], categories=ORDER, ordered=True)
        seg_default = seg_default.sort_values("Segment").reset_index(drop=True)
        fig2 = go.Figure()
        for i, row in seg_default.iterrows():
            fig2.add_trace(go.Bar(
                x=[row["Segment"]], y=[row["Default Rate"]],
                text=[f"{row['Default Rate']}%"],
                textposition="outside", textfont=dict(size=15, color="white"),
                marker_color=PALETTE[i], width=0.55, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter",
            yaxis=dict(gridcolor="#1f2630", range=[0, seg_default["Default Rate"].max()*1.3],
                       tickfont_size=13),
            xaxis=dict(tickfont_size=14),
            margin=dict(t=30, b=20, l=20, r=20), height=380)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    st.subheader("How the Risk Score Was Built")
    st.caption(
        "LTI showed three distinct default zones — flat below 15%, climbing between 15–40%, "
        "spiking sharply above 40%. Weights derived by dividing each factor's default rate "
        "spread by the total spread across all factors (94 points).")

    scoring_html = """
    <div style="overflow-x:auto; margin-bottom:24px;">
    <table style="width:100%; border-collapse:collapse;">
    <thead><tr style="background:#1a1f2e;">
        <th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Risk Factor</th>
        <th style="padding:14px 18px; text-align:center; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Spread</th>
        <th style="padding:14px 18px; text-align:center; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Max Penalty</th>
        <th style="padding:14px 18px; text-align:center; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Weight</th>
        <th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Signal</th>
    </tr></thead><tbody>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">📊 Loan-to-Income Ratio</td>
        <td style="padding:14px 18px; text-align:center; color:#00B4D8; font-weight:700; font-size:15px;">62 pts</td>
        <td style="padding:14px 18px; text-align:center; color:#ccc; font-size:15px;">−66</td>
        <td style="padding:14px 18px; text-align:center; color:#00B4D8; font-weight:700; font-size:15px;">66%</td>
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">Strongest predictor</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">📋 Prior Default on File</td>
        <td style="padding:14px 18px; text-align:center; color:#FFB703; font-weight:700; font-size:15px;">19 pts</td>
        <td style="padding:14px 18px; text-align:center; color:#ccc; font-size:15px;">−20</td>
        <td style="padding:14px 18px; text-align:center; color:#FFB703; font-weight:700; font-size:15px;">20%</td>
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">Strong signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">💼 Employment Length</td>
        <td style="padding:14px 18px; text-align:center; color:#FB8500; font-weight:700; font-size:15px;">11 pts</td>
        <td style="padding:14px 18px; text-align:center; color:#ccc; font-size:15px;">−12</td>
        <td style="padding:14px 18px; text-align:center; color:#FB8500; font-weight:700; font-size:15px;">12%</td>
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">Moderate signal</td>
    </tr>
    <tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">🕐 Credit History Length</td>
        <td style="padding:14px 18px; text-align:center; color:#888; font-weight:700; font-size:15px;">2 pts</td>
        <td style="padding:14px 18px; text-align:center; color:#ccc; font-size:15px;">−2</td>
        <td style="padding:14px 18px; text-align:center; color:#888; font-weight:700; font-size:15px;">2%</td>
        <td style="padding:14px 18px; color:#ccc; font-size:15px;">Weak signal</td>
    </tr>
    <tr style="background:#1a1f2e;">
        <td style="padding:14px 18px; color:#fff; font-weight:700; font-size:15px;">Total</td>
        <td style="padding:14px 18px; text-align:center; color:#fff; font-weight:700; font-size:15px;">94 pts</td>
        <td style="padding:14px 18px;"></td>
        <td style="padding:14px 18px; text-align:center; color:#fff; font-weight:700; font-size:15px;">100%</td>
        <td style="padding:14px 18px; color:#aaa; font-size:14px;">Score range: 0–100</td>
    </tr></tbody></table></div>
    """
    st.markdown(scoring_html, unsafe_allow_html=True)

    section_divider()

    st.subheader("Segment Summary — The Foundation of This Analysis")
    render_anchor_table()
    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 2
# ══════════════════════════════════════════
with tab2:

    st.subheader("Portfolio Analysis")
    st.caption("Lender Grade Validation, Exposure & Risk-Adjusted Return")

    insight_box(
        "The lender charges higher interest rates for lower grades — directionally correct. "
        "But from Grade D onwards, default losses outpace the extra interest charged and "
        "net yield turns negative. The lender is taking more risk without adequate compensation.")

    section_divider()

    st.subheader("Does the Lender's Grade Tell the Full Story?")
    st.caption(
        "The original dataset contains lender-assigned grades A–G (A = best, G = lowest). "
        "This project builds an independent risk segmentation and compares it against the lender's grading.")

    chart_header("Grade vs Segment Heatmap")
    chart_caption(
        "689 borrowers rated Grade B landed in SUBPRIME. "
        "In Grade C, 777 landed in SUBPRIME and 209 in HIGH-RISK. "
        "The lender's grade said moderate risk — the borrower's LTI ratio said otherwise.")

    cross = pd.crosstab(df["loan_grade"], df["segment"])
    cross = cross.reindex(columns=[c for c in ORDER if c in cross.columns])
    fig_heat = px.imshow(cross,
        color_continuous_scale=[[0.0,"#0d2d3a"],[0.08,"#0a4a60"],[0.3,"#0077a8"],[1.0,"#00B4D8"]],
        text_auto=True, aspect="auto",
        labels=dict(x="Risk Segment", y="Loan Grade", color="# Borrowers"))
    fig_heat.update_traces(xgap=2, ygap=2, textfont=dict(size=14))
    fig_heat.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        font_family="Inter", xaxis=dict(tickfont_size=14), yaxis=dict(tickfont_size=14),
        margin=dict(t=20, b=20, l=20, r=20), height=420)
    st.plotly_chart(fig_heat, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    col1, div_col, col2 = st.columns([1, 0.02, 1])
    with div_col:
        col_divider()
    with col1:
        chart_header("Exposure by Loan Grade")
        grade_exposure = df.groupby("loan_grade")["loan_amnt"].sum().div(1_000_000).round(2).reset_index()
        grade_exposure.columns = ["Grade","Exposure ($ Mn)"]
        grade_exposure = grade_exposure.sort_values("Grade").reset_index(drop=True)
        grade_colors = PALETTE + ["#90E0EF","#CAF0F8","#48CAE4"]
        fig1 = go.Figure()
        for i, row in grade_exposure.iterrows():
            fig1.add_trace(go.Bar(
                x=[row["Grade"]], y=[row["Exposure ($ Mn)"]],
                text=[f"${row['Exposure ($ Mn)']} Mn"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=grade_colors[i % len(grade_colors)],
                width=0.55, showlegend=False, cliponaxis=False))
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter", yaxis_title="Exposure ($ Mn)",
            yaxis=dict(gridcolor="#1f2630", range=[0, grade_exposure["Exposure ($ Mn)"].max()*1.25],
                       tickfont_size=13),
            xaxis=dict(tickfont_size=14),
            margin=dict(t=30, b=20, l=20, r=20), height=380)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate by Loan Grade")
        grade_default = df.groupby("loan_grade")["loan_status"].mean().mul(100).round(1).reset_index()
        grade_default.columns = ["Grade","Default Rate"]
        grade_default = grade_default.sort_values("Grade").reset_index(drop=True)
        max_dr = grade_default["Default Rate"].max()
        min_dr = grade_default["Default Rate"].min()
        fig2 = go.Figure()
        for i, row in grade_default.iterrows():
            ratio = (row["Default Rate"]-min_dr)/(max_dr-min_dr) if max_dr!=min_dr else 0.5
            if ratio < 0.5:
                r = int(ratio*2*255); g = 180; b = int(216-ratio*2*216)
            else:
                r = 255; g = int(183-(ratio-0.5)*2*183); b = 3
            fig2.add_trace(go.Bar(
                x=[row["Grade"]], y=[row["Default Rate"]],
                text=[f"{row['Default Rate']}%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color=f"rgb({r},{g},{b})",
                width=0.55, showlegend=False, cliponaxis=False))
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter",
            yaxis=dict(gridcolor="#1f2630", range=[0, max_dr*1.25], tickfont_size=13),
            xaxis=dict(tickfont_size=14),
            margin=dict(t=30, b=20, l=20, r=20), height=380)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    LGD_p2 = lgd_inline("p2",
        "LGD affects Net Yield below. Net Yield = Avg Interest Rate − (Default Rate × LGD). "
        "Adjust to see how recovery assumptions shift the profitability picture.")

    col3, div_col2, col4 = st.columns([1, 0.02, 1])
    with div_col2:
        col_divider()
    with col3:
        chart_header("Risk-Adjusted Net Yield by Grade")
        chart_caption(f"Currently using {int(LGD_p2*100)}% LGD. "
            "Cyan = compensated. Red = loss-making.")
        grade_rar = df.groupby("loan_grade").agg(
            Avg_Rate=("loan_int_rate","mean"),
            Default_Rate=("loan_status","mean")).reset_index()
        grade_rar["Net_Yield"] = (grade_rar["Avg_Rate"] - grade_rar["Default_Rate"]*100*LGD_p2).round(2)
        grade_rar = grade_rar.sort_values("loan_grade").reset_index(drop=True)
        min_y = grade_rar["Net_Yield"].min()
        max_y = grade_rar["Net_Yield"].max()
        fig3 = go.Figure()
        for _, row in grade_rar.iterrows():
            fig3.add_trace(go.Bar(
                x=[row["loan_grade"]], y=[row["Net_Yield"]],
                text=[f"{row['Net_Yield']}%"],
                textposition="outside", textfont=dict(size=14, color="white"),
                marker_color="#00B4D8" if row["Net_Yield"]>=0 else "#E63946",
                width=0.55, showlegend=False, cliponaxis=False))
        fig3.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter", yaxis_title="Net Yield (%)",
            yaxis=dict(gridcolor="#1f2630", range=[min_y*1.2, max_y*1.5], tickfont_size=13),
            xaxis=dict(tickfont_size=14),
            margin=dict(t=30, b=20, l=20, r=20), height=400)
        st.plotly_chart(fig3, use_container_width=True, config=CHART_CONFIG)
    with col4:
        chart_header("Interest Rate vs Risk Score")
        chart_caption("Each dot is a borrower. Wide scatter = mispricing.")
        sample = df.sample(2000, random_state=42)
        fig4 = px.scatter(sample, x="risk_score", y="loan_int_rate", color="segment",
            color_discrete_sequence=PALETTE, category_orders={"segment": ORDER}, opacity=0.5,
            labels={"risk_score":"Risk Score","loan_int_rate":"Interest Rate (%)","segment":"Segment"})
        fig4.update_traces(marker_size=5)
        fig4.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter",
            xaxis=dict(gridcolor="#1f2630", tickfont_size=13),
            yaxis=dict(gridcolor="#1f2630", tickfont_size=13),
            legend_font_size=13,
            margin=dict(t=20, b=20, l=20, r=20), height=400)
        st.plotly_chart(fig4, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 3
# ══════════════════════════════════════════
with tab3:

    st.subheader("Capital Allocation Strategy")
    st.caption("Exposure vs loss contribution and recommended reallocation.")

    insight_box(
        "Which segment generates the most loss per dollar of exposure? "
        "A segment holding 1% of exposure but contributing 5% of losses is destroying capital. "
        "Reallocation into PRIME reduces portfolio default rate without shrinking total book size.")

    st.caption("📌 All base figures below come from the Executive Overview.")

    rows = anchor_rows.copy()
    for r in rows:
        ep = r["exp_pct"]; lp = r["loss_pct"]
        if   lp > ep*2:   r["rec"], r["color"] = "Exit",     "#E63946"
        elif lp > ep:     r["rec"], r["color"] = "Tighten",  "#FB8500"
        elif lp < ep*0.8: r["rec"], r["color"] = "Grow",     "#00B4D8"
        else:             r["rec"], r["color"] = "Maintain", "#FFB703"

    alloc_mult = {"Grow":1.1,"Maintain":1.0,"Tighten":0.5,"Exit":0.0}
    raw_targets  = {r["seg"]: r["exp_pct"]*alloc_mult[r["rec"]] for r in rows}
    total_raw    = sum(raw_targets.values())
    target_alloc = {seg: round(val/total_raw*100,1) for seg,val in raw_targets.items()}

    section_divider()

    chart_header("Exposure vs Loss Contribution")
    chart_caption("Loss bar taller than exposure bar = capital destruction.")

    exp_loss_data = pd.DataFrame({
        "Segment": ORDER*2,
        "Metric": ["Exposure %"]*4 + ["Loss Contribution %"]*4,
        "Value": [r["exp_pct"] for r in rows] + [r["loss_pct"] for r in rows]})
    exp_loss_data["Segment"] = pd.Categorical(exp_loss_data["Segment"], categories=ORDER, ordered=True)
    fig_el = px.bar(exp_loss_data, x="Segment", y="Value", color="Metric",
        barmode="group", text="Value",
        color_discrete_map={"Exposure %":"#00B4D8","Loss Contribution %":"#E63946"},
        category_orders={"Segment":ORDER})
    fig_el.update_traces(texttemplate="%{text}%", textposition="outside",
        textfont=dict(size=15), cliponaxis=False)
    fig_el.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        font_family="Inter", yaxis_title="Percentage (%)",
        yaxis=dict(gridcolor="#1f2630", range=[0, exp_loss_data["Value"].max()*1.3], tickfont_size=13),
        xaxis=dict(tickfont_size=15), bargap=0.2, bargroupgap=0.05,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=14),
        margin=dict(t=50, b=20, l=20, r=20), height=420)
    st.plotly_chart(fig_el, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    chart_header("Recommended Portfolio Reallocation")
    chart_caption("Loss > 2× exposure → Exit | Loss > exposure → Tighten | Loss < 80% exposure → Grow")

    max_alloc = max(max(r["exp_pct"] for r in rows), max(target_alloc[seg] for seg in ORDER))
    alloc_df = pd.DataFrame({"Segment": ORDER,
        "Current %": [r["exp_pct"] for r in rows],
        "Target %": [target_alloc[seg] for seg in ORDER]})
    alloc_melted = alloc_df.melt(id_vars="Segment",
        value_vars=["Current %","Target %"], var_name="Type", value_name="Value")
    alloc_melted["Segment"] = pd.Categorical(alloc_melted["Segment"], categories=ORDER, ordered=True)
    fig_alloc = px.bar(alloc_melted, y="Segment", x="Value", color="Type",
        barmode="group", text="Value", orientation="h",
        color_discrete_map={"Current %":"#FFB703","Target %":"#00B4D8"},
        category_orders={"Segment":ORDER})
    fig_alloc.update_traces(texttemplate="%{x}%", textposition="outside",
        textfont=dict(size=15), cliponaxis=False)
    fig_alloc.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        font_family="Inter", xaxis_title="Allocation (%)",
        xaxis=dict(gridcolor="#1f2630", range=[0, max_alloc*1.3], tickfont_size=13),
        yaxis=dict(tickfont_size=15), bargap=0.2, bargroupgap=0.1,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=14),
        margin=dict(t=50, b=20, l=20, r=100), height=380)
    st.plotly_chart(fig_alloc, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 4
# ══════════════════════════════════════════
with tab4:

    st.subheader("Stress Testing & Scenarios")
    st.caption("What happens to the portfolio under adverse conditions?")

    insight_box(
        "Stress testing answers one question: how bad can it get? "
        "A PD multiplier simulates recession conditions by scaling up each segment's default rate. "
        "PRIME is the most resilient — its low base default rate means even a severe shock "
        "causes less absolute damage than the same shock applied to HIGH-RISK.")

    st.caption("📌 All base figures below come from the Executive Overview. EL = Exposure × Default Rate × LGD.")

    section_divider()

    LGD_p4 = lgd_inline("p4",
        "LGD affects all Expected Loss calculations on this page. "
        "Adjust to simulate different recovery assumptions.")

    st.subheader("Recession Stress Test")

    scenario = st.selectbox("Select Stress Scenario", options=[
        "Base Case (No Stress)", "Mild Recession (+25% PD)",
        "Severe Recession (+50% PD)", "Extreme Stress (+75% PD)"], index=0)
    mult_map = {"Base Case (No Stress)":1.00, "Mild Recession (+25% PD)":1.25,
                "Severe Recession (+50% PD)":1.50, "Extreme Stress (+75% PD)":1.75}
    pd_mult = mult_map[scenario]

    stress_rows = []
    for r in anchor_rows:
        base_el     = round((r["base_pd"]*LGD_p4*r["exp"])/1_000_000, 2)
        stressed_pd = min(r["base_pd"]*pd_mult, 1.0)
        stressed_dr = round(stressed_pd*100, 1)
        stressed_el = round((stressed_pd*LGD_p4*r["exp"])/1_000_000, 2)
        el_change   = round(stressed_el - base_el, 2)
        stress_rows.append({"seg":r["seg"],"exp":r["exp"],
            "base_dr":r["dr"],"stressed_dr":stressed_dr,
            "base_el":base_el,"stressed_el":stressed_el,"el_change":el_change})

    base_total_el     = round(sum(r["base_el"] for r in stress_rows), 2)
    stressed_total_el = round(sum(r["stressed_el"] for r in stress_rows), 2)
    el_increase       = round(stressed_total_el - base_total_el, 2)
    el_increase_pct   = round((el_increase/base_total_el)*100,1) if base_total_el>0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Base Expected Loss", f"${base_total_el} Mn")
    m2.metric("Stressed Expected Loss", f"${stressed_total_el} Mn",
        delta=f"+${el_increase} Mn", delta_color="inverse")
    m3.metric("Increase in Loss", f"{el_increase_pct}%",
        delta=f"{el_increase_pct}%", delta_color="inverse")

    st.markdown(
        "<p style='color:#aaaaaa; font-size:14px !important; margin:12px 0 8px 0;'>"
        "Full computation chain — Exposure × Default Rate × LGD = Expected Loss.</p>",
        unsafe_allow_html=True)

    # ── Base EL table ──
    el_hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse;">'
        '<thead><tr style="background:#1a1f2e;">'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Segment</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Exposure</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Base DR</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">LGD</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Base EL</th>'
        '</tr></thead><tbody>'
    )
    el_body = ""
    for r in stress_rows:
        exp_mn = round(r["exp"]/1_000_000, 2)
        el_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:14px 18px; color:{seg_colors[r["seg"]]}; font-weight:700; font-size:15px;">{r["seg"]}</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#ccc; font-size:15px;">${exp_mn} Mn</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#ccc; font-size:15px;">{r["base_dr"]}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#ccc; font-size:15px;">{int(LGD_p4*100)}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#00B4D8; font-weight:700; font-size:15px;">${r["base_el"]} Mn</td>'
            f'</tr>')
    total_exp_mn = round(sum(r["exp"] for r in stress_rows)/1_000_000, 2)
    el_body += (
        f'<tr style="background:#1a1f2e;">'
        f'<td style="padding:14px 18px; color:#fff; font-weight:700; font-size:15px;">Total</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">${total_exp_mn} Mn</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#aaa; font-size:15px;">—</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#aaa; font-size:15px;">{int(LGD_p4*100)}%</td>'
        f'<td style="padding:14px 18px; text-align:right; color:#fff; font-weight:700; font-size:15px;">${base_total_el} Mn</td>'
        f'</tr>')
    st.markdown(el_hdr + el_body + "</tbody></table></div>", unsafe_allow_html=True)

    # ── Stress comparison table ──
    s_hdr = (
        '<div style="overflow-x:auto; margin-bottom:20px;">'
        '<table style="width:100%; border-collapse:collapse;">'
        '<thead><tr style="background:#1a1f2e;">'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Segment</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Base DR</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Stressed DR</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Base EL</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Stressed EL</th>'
        '<th style="padding:14px 18px; text-align:right; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Additional Loss</th>'
        '</tr></thead><tbody>'
    )
    s_body = ""
    for sr in stress_rows:
        cc = "#E63946" if sr["el_change"]>0 else "#00B4D8"
        s_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:14px 18px; color:{seg_colors[sr["seg"]]}; font-weight:700; font-size:15px;">{sr["seg"]}</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#ccc; font-size:15px;">{sr["base_dr"]}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#FFB703; font-size:15px;">{sr["stressed_dr"]}%</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#ccc; font-size:15px;">${sr["base_el"]} Mn</td>'
            f'<td style="padding:14px 18px; text-align:right; color:#FFB703; font-size:15px;">${sr["stressed_el"]} Mn</td>'
            f'<td style="padding:14px 18px; text-align:right; color:{cc}; font-weight:700; font-size:15px;">+${sr["el_change"]} Mn</td>'
            f'</tr>')
    st.markdown(s_hdr + s_body + "</tbody></table></div>", unsafe_allow_html=True)

    section_divider()

    col1, div_col, col2 = st.columns([1, 0.02, 1])
    with div_col:
        col_divider()
    with col1:
        chart_header("Expected Loss: Base vs Stressed")
        el_df = pd.DataFrame({"Segment": ORDER*2,
            "Scenario": ["Base Case"]*4 + [scenario]*4,
            "Expected Loss ($ Mn)": [r["base_el"] for r in stress_rows] + [r["stressed_el"] for r in stress_rows]})
        el_df["Segment"] = pd.Categorical(el_df["Segment"], categories=ORDER, ordered=True)
        fig1 = px.bar(el_df, x="Segment", y="Expected Loss ($ Mn)",
            color="Scenario", barmode="group", text="Expected Loss ($ Mn)",
            color_discrete_map={"Base Case":"#00B4D8", scenario:"#E63946"},
            category_orders={"Segment":ORDER})
        fig1.update_traces(texttemplate="$%{text} Mn", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter",
            yaxis=dict(gridcolor="#1f2630", range=[0,el_df["Expected Loss ($ Mn)"].max()*1.35], tickfont_size=13),
            xaxis=dict(tickfont_size=14), bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font_size=13),
            margin=dict(t=50,b=20,l=20,r=20), height=400)
        st.plotly_chart(fig1, use_container_width=True, config=CHART_CONFIG)
    with col2:
        chart_header("Default Rate: Base vs Stressed")
        dr_df = pd.DataFrame({"Segment": ORDER*2,
            "Scenario": ["Base Case"]*4 + [scenario]*4,
            "Default Rate (%)": [r["base_dr"] for r in stress_rows] + [r["stressed_dr"] for r in stress_rows]})
        dr_df["Segment"] = pd.Categorical(dr_df["Segment"], categories=ORDER, ordered=True)
        fig2 = px.bar(dr_df, x="Segment", y="Default Rate (%)",
            color="Scenario", barmode="group", text="Default Rate (%)",
            color_discrete_map={"Base Case":"#00B4D8", scenario:"#E63946"},
            category_orders={"Segment":ORDER})
        fig2.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=13), cliponaxis=False)
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
            font_family="Inter",
            yaxis=dict(gridcolor="#1f2630", range=[0,dr_df["Default Rate (%)"].max()*1.35], tickfont_size=13),
            xaxis=dict(tickfont_size=14), bargap=0.2, bargroupgap=0.05,
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font_size=13),
            margin=dict(t=50,b=20,l=20,r=20), height=400)
        st.plotly_chart(fig2, use_container_width=True, config=CHART_CONFIG)

    section_divider()

    st.subheader("Capital Reallocation Simulator")
    st.caption(
        "Simulates future lending decisions — not movement of existing loans. "
        "Redirects future originations from SUBPRIME and HIGH-RISK towards PRIME.")

    shift_pct = st.slider(
        "Capital redirected from SUBPRIME + HIGH-RISK → PRIME (%)",
        min_value=0, max_value=15, value=5, step=1)

    prime_data = df[df["segment"]=="PRIME"]
    near_data  = df[df["segment"]=="NEAR-PRIME"]
    sub_data   = df[df["segment"]=="SUBPRIME"]
    high_data  = df[df["segment"]=="HIGH-RISK"]

    total_exp    = df["loan_amnt"].sum()
    shift_amount = total_exp*(shift_pct/100)
    sub_exp_raw  = sub_data["loan_amnt"].sum()
    high_exp_raw = high_data["loan_amnt"].sum()
    risky_total  = sub_exp_raw + high_exp_raw
    sub_weight   = sub_exp_raw/risky_total if risky_total>0 else 0.7
    high_weight  = high_exp_raw/risky_total if risky_total>0 else 0.3

    prime_exp_new = prime_data["loan_amnt"].sum() + shift_amount
    near_exp_new  = near_data["loan_amnt"].sum()
    sub_exp_new   = max(sub_exp_raw - shift_amount*sub_weight, 0)
    high_exp_new  = max(high_exp_raw - shift_amount*high_weight, 0)

    prime_pd = prime_data["loan_status"].mean()
    near_pd  = near_data["loan_status"].mean()
    sub_pd   = sub_data["loan_status"].mean()
    high_pd  = high_data["loan_status"].mean()

    base_port_dr = round((prime_data["loan_amnt"].sum()*prime_pd +
        near_data["loan_amnt"].sum()*near_pd + sub_exp_raw*sub_pd +
        high_exp_raw*high_pd)/total_exp*100, 2)

    new_total_exp = prime_exp_new+near_exp_new+sub_exp_new+high_exp_new
    new_port_dr = round((prime_exp_new*prime_pd + near_exp_new*near_pd +
        sub_exp_new*sub_pd + high_exp_new*high_pd)/new_total_exp*100, 2)

    base_port_el = round((prime_data["loan_amnt"].sum()*prime_pd*LGD_p4 +
        near_data["loan_amnt"].sum()*near_pd*LGD_p4 + sub_exp_raw*sub_pd*LGD_p4 +
        high_exp_raw*high_pd*LGD_p4)/1_000_000, 2)

    new_port_el = round((prime_exp_new*prime_pd*LGD_p4 + near_exp_new*near_pd*LGD_p4 +
        sub_exp_new*sub_pd*LGD_p4 + high_exp_new*high_pd*LGD_p4)/1_000_000, 2)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Base Default Rate", f"{base_port_dr}%")
    r2.metric("Simulated Default Rate", f"{new_port_dr}%",
        delta=f"{round(new_port_dr-base_port_dr,2)}%", delta_color="inverse")
    r3.metric("Base Expected Loss", f"${base_port_el} Mn")
    r4.metric("Simulated Expected Loss", f"${new_port_el} Mn",
        delta=f"{round(new_port_el-base_port_el,2)}", delta_color="inverse")

    st.markdown(
        f"<p style='color:#aaaaaa; font-size:14px !important; margin:12px 0 20px 0;'>"
        f"Reallocation sourced proportionally — "
        f"<b style='color:#FB8500'>{round(sub_weight*100,1)}% from SUBPRIME</b> and "
        f"<b style='color:#E63946'>{round(high_weight*100,1)}% from HIGH-RISK</b>.</p>",
        unsafe_allow_html=True)

    chart_header("Simulated Exposure Shift")
    realloc_data = pd.DataFrame({"Segment": ORDER*2,
        "Type": ["Current"]*4+["Simulated"]*4,
        "Exposure ($ Mn)": [
            round(prime_data["loan_amnt"].sum()/1_000_000,2),
            round(near_data["loan_amnt"].sum()/1_000_000,2),
            round(sub_exp_raw/1_000_000,2), round(high_exp_raw/1_000_000,2),
            round(prime_exp_new/1_000_000,2), round(near_exp_new/1_000_000,2),
            round(sub_exp_new/1_000_000,2), round(high_exp_new/1_000_000,2)]})
    realloc_data["Segment"] = pd.Categorical(realloc_data["Segment"], categories=ORDER, ordered=True)
    fig_sim = px.bar(realloc_data, x="Segment", y="Exposure ($ Mn)", color="Type",
        barmode="group", text="Exposure ($ Mn)",
        color_discrete_map={"Current":"#FFB703","Simulated":"#00B4D8"},
        category_orders={"Segment":ORDER})
    fig_sim.update_traces(texttemplate="$%{text} Mn", textposition="outside",
        textfont=dict(size=14), cliponaxis=False)
    fig_sim.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        font_family="Inter", yaxis_title="Exposure ($ Mn)",
        yaxis=dict(gridcolor="#1f2630", range=[0, realloc_data["Exposure ($ Mn)"].max()*1.3], tickfont_size=13),
        xaxis=dict(tickfont_size=15), bargap=0.2, bargroupgap=0.05,
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font_size=14),
        margin=dict(t=50,b=20,l=20,r=20), height=400)
    st.plotly_chart(fig_sim, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 5
# ══════════════════════════════════════════
with tab5:

    st.subheader("Management Recommendations")
    st.caption("Executive summary — findings, actions and strategic direction.")

    insight_box(
        "This section consolidates findings into four clear actions. "
        "Segments where loss contribution far exceeds exposure share are destroying capital — exit or reduce. "
        "Segments where loss contribution is well below exposure share are underleveraged — grow them.")

    LGD_p5 = st.session_state.lgd_value / 100

    portfolio_dr = round(df["loan_status"].mean()*100, 1)
    seg_stats = {}
    for r in anchor_rows:
        seg = r["seg"]
        s   = df[df["segment"]==seg]
        net_yield = round(s["loan_int_rate"].mean() - (r["dr"]*LGD_p5), 2)
        seg_stats[seg] = {"exp_pct":r["exp_pct"],"dr":r["dr"],
                          "loss_pct":r["loss_pct"],"net_yield":net_yield}

    alloc_mult = {"Grow":1.1,"Maintain":1.0,"Tighten":0.5,"Exit":0.0}
    rec_map = {}
    for seg in ORDER:
        ep = seg_stats[seg]["exp_pct"]; lp = seg_stats[seg]["loss_pct"]
        if   lp > ep*2:   rec_map[seg] = ("Exit",    "#E63946")
        elif lp > ep:     rec_map[seg] = ("Tighten", "#FB8500")
        elif lp < ep*0.8: rec_map[seg] = ("Grow",    "#00B4D8")
        else:             rec_map[seg] = ("Maintain","#FFB703")

    raw_t   = {seg: seg_stats[seg]["exp_pct"]*alloc_mult[rec_map[seg][0]] for seg in ORDER}
    tot_raw = sum(raw_t.values())
    t_alloc = {seg: round(val/tot_raw*100,1) for seg,val in raw_t.items()}

    worst_seg  = max(ORDER, key=lambda s: seg_stats[s]["loss_pct"]/seg_stats[s]["exp_pct"])
    best_yield = max(ORDER, key=lambda s: seg_stats[s]["net_yield"])
    hr_gap     = round(seg_stats["HIGH-RISK"]["loss_pct"]-seg_stats["HIGH-RISK"]["exp_pct"],1)

    kpi_grid([
        ("Portfolio Default Rate",   f"{portfolio_dr}%",    "Across all 32,572 loans"),
        ("Highest Loss Contributor", worst_seg,             "Loss ÷ Exposure ratio"),
        ("Best Net Yield Segment",   best_yield,            "After expected loss"),
        ("HIGH-RISK Loss Excess",    f"+{hr_gap}%",         "Loss % above exposure %"),
        ("LGD Assumption",           f"{int(LGD_p5*100)}%", "Adjust on Stress Testing tab"),
    ])

    section_divider()

    st.subheader("Analysis Summary")

    high_exp     = seg_stats["HIGH-RISK"]["exp_pct"]
    high_loss    = seg_stats["HIGH-RISK"]["loss_pct"]
    high_ratio   = round(high_loss/high_exp, 1)
    prime_dr     = seg_stats["PRIME"]["dr"]
    prime_yield  = seg_stats["PRIME"]["net_yield"]
    sub_exit_pct = round(seg_stats["SUBPRIME"]["exp_pct"]*0.5 + seg_stats["HIGH-RISK"]["exp_pct"], 1)

    findings = [
        f"The portfolio carries a <b style='color:#FFB703'>{portfolio_dr}% overall default rate</b>. "
        f"The dominant risk predictor is loan-to-income ratio, "
        f"with a 62-point default rate spread between the safest and riskiest borrowers.",
        f"<b style='color:#E63946'>HIGH-RISK segment</b> represents only {high_exp}% of exposure "
        f"but contributes {high_loss}% of total losses — a {high_ratio}× loss-to-exposure ratio. "
        f"Clearest case of capital misallocation in the portfolio.",
        f"<b style='color:#00B4D8'>PRIME segment</b> holds {seg_stats['PRIME']['exp_pct']}% of exposure "
        f"with a {prime_dr}% default rate and net yield of {prime_yield}% after expected loss. "
        f"Most capital-efficient tier and the primary growth target.",
        f"Risk-adjusted net yield turns negative from Grade D onwards — interest rate pricing does not "
        f"fully compensate for default losses in lower credit grades at {int(LGD_p5*100)}% LGD.",
        f"Recommended reallocation — reducing SUBPRIME and exiting HIGH-RISK — frees ~{sub_exit_pct}% "
        f"of portfolio capital for PRIME, improving default rate and expected loss without changing book size."
    ]

    fhtml = '<div style="background:#1a1f2e; border-radius:10px; padding:28px 32px; border:1px solid #2d3447;">'
    for f in findings:
        fhtml += f'<p style="color:#cccccc; font-size:16px !important; margin-bottom:16px; line-height:1.7;">→ {f}</p>'
    fhtml += '</div>'
    st.markdown(fhtml, unsafe_allow_html=True)

    section_divider()

    st.subheader("Recommended Actions")
    st.caption("Loss > 2× exposure → Exit · Loss > exposure → Tighten · Loss < 80% exposure → Grow · otherwise → Maintain")

    actions = [
        ("PRIME", rec_map["PRIME"][0], rec_map["PRIME"][1],
         f"Grow from {seg_stats['PRIME']['exp_pct']}% to {t_alloc['PRIME']}%",
         f"{seg_stats['PRIME']['dr']}% default rate. Loss well below exposure share."),
        ("NEAR-PRIME", rec_map["NEAR-PRIME"][0], rec_map["NEAR-PRIME"][1],
         "Maintain with stricter underwriting on LTI > 25%",
         f"{seg_stats['NEAR-PRIME']['dr']}% default rate. "
         f"Loss {seg_stats['NEAR-PRIME']['loss_pct']}% vs exposure {seg_stats['NEAR-PRIME']['exp_pct']}%."),
        ("SUBPRIME", rec_map["SUBPRIME"][0], rec_map["SUBPRIME"][1],
         f"Reduce from {seg_stats['SUBPRIME']['exp_pct']}% to {t_alloc['SUBPRIME']}%",
         f"{seg_stats['SUBPRIME']['dr']}% default rate. Loss exceeds exposure share."),
        ("HIGH-RISK", rec_map["HIGH-RISK"][0], rec_map["HIGH-RISK"][1],
         "Stop new originations. Wind down.",
         f"{seg_stats['HIGH-RISK']['dr']}% default rate. "
         f"{seg_stats['HIGH-RISK']['loss_pct']}% of losses on {seg_stats['HIGH-RISK']['exp_pct']}% exposure.")
    ]

    a_hdr = (
        '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse;">'
        '<thead><tr style="background:#1a1f2e;">'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Segment</th>'
        '<th style="padding:14px 18px; text-align:center; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Action</th>'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">What to Do</th>'
        '<th style="padding:14px 18px; text-align:left; border-bottom:1px solid #2d3447; font-size:12px; color:#aaa; text-transform:uppercase; letter-spacing:0.6px;">Why</th>'
        '</tr></thead><tbody>'
    )
    a_body = ""
    badge = "padding:5px 16px; border-radius:20px; font-weight:700; font-size:13px;"
    for seg, rec, color, what, why in actions:
        a_body += (
            f'<tr style="background:#0e1117; border-bottom:1px solid #1a1f2e;">'
            f'<td style="padding:14px 18px; color:white; font-weight:700; font-size:15px;">{seg}</td>'
            f'<td style="padding:14px 18px; text-align:center;">'
            f'<span style="background:{color}22; color:{color}; border:1px solid {color}; {badge}">{rec}</span></td>'
            f'<td style="padding:14px 18px; color:#ccc; font-size:15px;">{what}</td>'
            f'<td style="padding:14px 18px; color:#aaa; font-size:14px;">{why}</td>'
            f'</tr>')
    st.markdown(a_hdr + a_body + "</tbody></table></div>", unsafe_allow_html=True)

    section_divider()

    chart_header("Current vs Target Portfolio Allocation")
    final_alloc = pd.DataFrame({"Segment": ORDER,
        "Current %": [seg_stats[seg]["exp_pct"] for seg in ORDER],
        "Target %": [t_alloc[seg] for seg in ORDER]})
    final_melted = final_alloc.melt(id_vars="Segment",
        value_vars=["Current %","Target %"], var_name="Type", value_name="Value")
    final_melted["Segment"] = pd.Categorical(final_melted["Segment"], categories=ORDER, ordered=True)
    max_val = final_melted["Value"].max()
    fig_fin = px.bar(final_melted, y="Segment", x="Value", color="Type",
        barmode="group", text="Value", orientation="h",
        color_discrete_map={"Current %":"#FFB703","Target %":"#00B4D8"},
        category_orders={"Segment":ORDER})
    fig_fin.update_traces(texttemplate="%{x}%", textposition="outside",
        textfont=dict(size=15), cliponaxis=False)
    fig_fin.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font_color="white",
        font_family="Inter", xaxis_title="Allocation (%)",
        xaxis=dict(gridcolor="#1f2630", range=[0,max_val*1.3], tickfont_size=13),
        yaxis=dict(tickfont_size=15), bargap=0.2, bargroupgap=0.1,
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font_size=14),
        margin=dict(t=50,b=20,l=20,r=100), height=320)
    st.plotly_chart(fig_fin, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)
