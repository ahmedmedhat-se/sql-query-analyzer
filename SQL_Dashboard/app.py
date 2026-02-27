import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Performance Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

/* ═══════════ BASE ═══════════ */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #060d1f !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}
[data-testid="stHeader"] { background: #060d1f !important; border-bottom: 1px solid #0f1f3d; }
[data-testid="stSidebar"] > div:first-child {
    background: #07112a !important;
    border-right: 1px solid #0f1f3d;
}
.block-container { padding: 2.5rem 2.5rem 4rem !important; max-width: 1400px; }

/* ═══════════ SIDEBAR ═══════════ */
.sidebar-logo {
    display: flex; align-items: center; gap: 12px;
    padding: 1.2rem 0 2rem 0;
    border-bottom: 1px solid #0f1f3d;
    margin-bottom: 1.5rem;
}
.sidebar-logo-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 800; color: #fff;
}
.sidebar-logo-text { font-size: 1rem; font-weight: 700; color: #fff; line-height: 1.2; }
.sidebar-logo-sub { font-size: 0.7rem; color: #3b82f6; font-family: 'JetBrains Mono', monospace; }

.nav-section-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    color: #334155; text-transform: uppercase;
    margin: 1.5rem 0 0.6rem 0; padding: 0;
}

.sidebar-stat {
    background: #0d1e3d; border: 1px solid #1a3060;
    border-radius: 12px; padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.sidebar-stat-label { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
.sidebar-stat-value { font-size: 1.4rem; font-weight: 800; color: #3b82f6; font-family: 'JetBrains Mono', monospace; margin-top: 2px; }

.sidebar-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px; }
.badge-good { background: rgba(34,197,94,0.1); color: #22c55e; border: 1px solid rgba(34,197,94,0.2); }
.badge-warn { background: rgba(251,191,36,0.1); color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
.badge-bad  { background: rgba(239,68,68,0.1);  color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }

/* ═══════════ PAGE HEADER ═══════════ */
.page-header {
    display: flex; align-items: flex-end; justify-content: space-between;
    margin-bottom: 2rem;
    animation: fadeSlideDown 0.5s ease both;
}
.page-title { font-size: 2rem; font-weight: 900; color: #fff; letter-spacing: -1px; line-height: 1.1; }
.page-title span { color: #3b82f6; }
.page-subtitle { font-size: 0.85rem; color: #475569; margin-top: 0.3rem; font-family: 'JetBrains Mono', monospace; }
.live-badge {
    display: flex; align-items: center; gap: 6px;
    background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2);
    border-radius: 20px; padding: 6px 14px;
    font-size: 0.75rem; font-weight: 600; color: #22c55e;
}
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; animation: pulse 1.8s infinite; }

/* ═══════════ KPI CARDS ═══════════ */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 2rem; }
.kpi-card {
    background: #0a1628; border: 1px solid #0f1f3d;
    border-radius: 16px; padding: 1.6rem 1.8rem;
    position: relative; overflow: hidden;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
    animation: fadeSlideUp 0.5s ease both;
}
.kpi-card:nth-child(1){animation-delay:0.05s}
.kpi-card:nth-child(2){animation-delay:0.10s}
.kpi-card:nth-child(3){animation-delay:0.15s}
.kpi-card:nth-child(4){animation-delay:0.20s}
.kpi-card:hover { border-color: #3b82f6; transform: translateY(-4px); box-shadow: 0 16px 40px rgba(59,130,246,0.12); }
.kpi-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0; opacity: 0; transition: opacity 0.25s;
}
.kpi-card:hover::after { opacity: 1; }
.kpi-card.blue::after   { background: #3b82f6; }
.kpi-card.cyan::after   { background: #06b6d4; }
.kpi-card.green::after  { background: #22c55e; }
.kpi-card.purple::after { background: #8b5cf6; }

.kpi-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 1rem; }
.kpi-icon.blue   { background: rgba(59,130,246,0.12); }
.kpi-icon.cyan   { background: rgba(6,182,212,0.12);  }
.kpi-icon.green  { background: rgba(34,197,94,0.12);  }
.kpi-icon.purple { background: rgba(139,92,246,0.12); }

.kpi-label { font-size: 0.72rem; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.kpi-value { font-size: 2.5rem; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1; margin: 0.3rem 0 0.5rem; font-family: 'JetBrains Mono', monospace; }
.kpi-value.blue   { color: #3b82f6; }
.kpi-value.cyan   { color: #06b6d4; }
.kpi-value.green  { color: #22c55e; }
.kpi-value.purple { color: #8b5cf6; }
.kpi-sub { font-size: 0.75rem; color: #334155; }

/* ═══════════ SECTION TITLE ═══════════ */
.sec-title {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; color: #334155; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 10px;
}
.sec-title::after { content: ''; flex: 1; height: 1px; background: #0f1f3d; }

/* ═══════════ TABS ═══════════ */
[data-testid="stTabs"] [role="tablist"] { gap: 4px; border-bottom: 1px solid #0f1f3d !important; }
[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
    font-size: 0.82rem !important; color: #475569 !important;
    padding: 0.55rem 1.1rem !important; border-radius: 8px 8px 0 0 !important;
    transition: color 0.2s, background 0.2s !important;
    border: none !important; background: transparent !important;
}
[data-testid="stTabs"] button:hover { color: #94a3b8 !important; background: rgba(255,255,255,0.03) !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3b82f6 !important;
    background: rgba(59,130,246,0.07) !important;
    border-bottom: 2px solid #3b82f6 !important;
}

/* ═══════════ DATAFRAME ═══════════ */
[data-testid="stDataFrame"] { border: 1px solid #0f1f3d !important; border-radius: 14px !important; overflow: hidden; }

/* ═══════════ RADIO ═══════════ */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { display: flex; gap: 8px; flex-wrap: wrap; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: #0a1628 !important; border: 1px solid #0f1f3d !important;
    border-radius: 8px !important; padding: 6px 16px !important;
    font-size: 0.8rem !important; font-weight: 600 !important; color: #475569 !important;
    cursor: pointer; transition: all 0.2s;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: rgba(59,130,246,0.1) !important;
    border-color: #3b82f6 !important; color: #3b82f6 !important;
}

/* ═══════════ METRIC (fallback for Audit tab) ═══════════ */
[data-testid="stMetric"] {
    background: #0a1628 !important; border: 1px solid #0f1f3d !important;
    border-radius: 12px !important; padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] { color: #3b82f6 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 1.6rem !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #475569 !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; }

/* ═══════════ SCROLLBAR ═══════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060d1f; }
::-webkit-scrollbar-thumb { background: #1a3060; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3b82f6; }

/* ═══════════ ANIMATIONS ═══════════ */
@keyframes fadeSlideDown { from{opacity:0;transform:translateY(-16px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeSlideUp   { from{opacity:0;transform:translateY(20px)}  to{opacity:1;transform:translateY(0)} }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.8)} }

hr { border-color: #0f1f3d !important; margin: 1.5rem 0 !important; }
[data-testid="stAlert"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Chart layout helper ───────────────────────────────────────────────────────
def chart_layout(**kwargs):
    base = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#64748b", size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="#0f1f3d", zeroline=False, showline=False),
        yaxis=dict(gridcolor="#0f1f3d", zeroline=False, showline=False),
    )
    base.update(kwargs)
    return base

# ── Data ─────────────────────────────────────────────────────────────────────
# ── Data Loading Optimized ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    # 1. قائمة بالمسارات المحتملة (عشان نضمن إنه يلقط الملف)
    possible_paths = [
        "SQL_Performance_Analysis.csv",                            # لو الملف بره جنب app.py
        "SQL_dashboard/SQL_Performance_Analysis.csv",              # لو جوه فولدر حرف D كبير
        "sql_dashboard/SQL_Performance_Analysis.csv",              # لو جوه فولدر حرف d صغير
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            # لو نجح في القراءة، نكسر الحلقة
            break 
        except FileNotFoundError:
            continue
            
    if df is None:
        raise FileNotFoundError("Could not find SQL_Performance_Analysis.csv in any expected location.")

    # التنظيف والتحويل
    numeric_cols = ["execution_time_ms", "rows_examined", "rows_returned", "complexity_score"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    df['index_status'] = df['index_used'].apply(
        lambda x: 'Indexed' if "PRIMARY" in str(x).upper() or str(x) == "1" else 'Non-Indexed'
    )
    df["efficiency_ratio"] = (df["rows_returned"] / (df["rows_examined"] + 1)).clip(upper=1)
    
    if 'id_x' not in df.columns:
        df['id_x'] = range(1, len(df) + 1)
        
    return df

try:
    df = load_data()

    # ═══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">⚡</div>
            <div>
                <div class="sidebar-logo-text">SQL Pro</div>
                <div class="sidebar-logo-sub">v2.1 · Enterprise</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section-label">Navigation</div>', unsafe_allow_html=True)
        page = st.radio("", ["📊  Overview", "📉  Charts", "🔍  Workload", "📑  Audit Log"], label_visibility="collapsed")

        st.markdown('<div class="nav-section-label">Filter</div>', unsafe_allow_html=True)
        filter_choice = st.radio("", ["All Queries", "Top 5 Slowest", "Top 5 Most Efficient"], label_visibility="collapsed")

        # Quick stats
        idx_rate = (df['index_status'] == 'Indexed').mean() * 100
        avg_lat  = df['execution_time_ms'].mean()
        eff      = df['efficiency_ratio'].mean() * 100

        health_badge = '<span class="sidebar-badge badge-good">Healthy</span>'   if eff > 70 \
                  else '<span class="sidebar-badge badge-warn">Degraded</span>'  if eff > 40 \
                  else '<span class="sidebar-badge badge-bad">Critical</span>'
        lat_badge    = '<span class="sidebar-badge badge-good">Fast</span>'      if avg_lat < 200 \
                  else '<span class="sidebar-badge badge-warn">Moderate</span>'  if avg_lat < 1000 \
                  else '<span class="sidebar-badge badge-bad">Slow</span>'

        st.markdown('<div class="nav-section-label">Quick Stats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sidebar-stat">
            <div class="sidebar-stat-label">Total Queries</div>
            <div class="sidebar-stat-value">{len(df):,}</div>
        </div>
        <div class="sidebar-stat">
            <div class="sidebar-stat-label">Avg Latency · {lat_badge}</div>
            <div class="sidebar-stat-value">{avg_lat:.0f}<span style="font-size:0.9rem;color:#334155"> ms</span></div>
        </div>
        <div class="sidebar-stat">
            <div class="sidebar-stat-label">Efficiency · {health_badge}</div>
            <div class="sidebar-stat-value">{eff:.1f}<span style="font-size:0.9rem;color:#334155"> %</span></div>
        </div>
        <div class="sidebar-stat">
            <div class="sidebar-stat-label">Index Coverage</div>
            <div class="sidebar-stat-value">{idx_rate:.0f}<span style="font-size:0.9rem;color:#334155"> %</span></div>
        </div>
        """, unsafe_allow_html=True)

    # ── Filtered df ────────────────────────────────────────────────────────────
    if "Slowest" in filter_choice:
        display_df = df.nlargest(5, "execution_time_ms")
    elif "Efficient" in filter_choice:
        display_df = df.nlargest(5, "efficiency_ratio")
    else:
        display_df = df

    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    active_page = page.split("  ")[-1]
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">SQL <span>Performance</span> Dashboard</div>
            <div class="page-subtitle">enterprise · {active_page.lower()} · {len(display_df)} queries shown</div>
        </div>
        <div class="live-badge"><div class="live-dot"></div> Live Monitoring</div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # KPI CARDS (always visible)
    # ═══════════════════════════════════════════════════════════════════════════
    max_lat = display_df['execution_time_ms'].max()
    min_lat = display_df['execution_time_ms'].min()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-icon blue">📊</div>
            <div class="kpi-label">Total Queries</div>
            <div class="kpi-value blue">{len(display_df):,}</div>
            <div class="kpi-sub">in current view</div>
        </div>
        <div class="kpi-card cyan">
            <div class="kpi-icon cyan">⚡</div>
            <div class="kpi-label">Avg Latency</div>
            <div class="kpi-value cyan">{display_df['execution_time_ms'].mean():.0f}<span style="font-size:1.2rem"> ms</span></div>
            <div class="kpi-sub">range {min_lat:.0f} – {max_lat:.0f} ms</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-icon green">🛡️</div>
            <div class="kpi-label">Index Coverage</div>
            <div class="kpi-value green">{(df['index_status']=='Indexed').mean()*100:.0f}<span style="font-size:1.2rem"> %</span></div>
            <div class="kpi-sub">{(df['index_status']=='Indexed').sum()} indexed queries</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-icon purple">🎯</div>
            <div class="kpi-label">System Efficiency</div>
            <div class="kpi-value purple">{display_df['efficiency_ratio'].mean()*100:.1f}<span style="font-size:1.2rem"> %</span></div>
            <div class="kpi-sub">rows returned / examined</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # PAGES
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Overview ──────────────────────────────────────────────────────────────
    if "Overview" in page:
        col_a, col_b = st.columns([3, 2], gap="large")

        with col_a:
            st.markdown('<div class="sec-title">Execution Time vs Rows Examined</div>', unsafe_allow_html=True)
            fig = px.scatter(
                display_df, x="rows_examined", y="execution_time_ms",
                size="rows_returned", color="efficiency_ratio",
                color_continuous_scale=[[0,"#ef4444"],[0.5,"#3b82f6"],[1,"#22c55e"]],
                labels={"rows_examined":"Rows Examined","execution_time_ms":"Latency (ms)","efficiency_ratio":"Efficiency"},
                hover_data=["complexity_score","index_status"],
            )
            fig.update_traces(marker=dict(line=dict(width=0), opacity=0.85))
            fig.update_layout(**chart_layout(height=320,
                coloraxis_colorbar=dict(thickness=8, tickfont=dict(size=9), title=dict(text="Eff.", font=dict(size=10)))))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown('<div class="sec-title">Index Usage</div>', unsafe_allow_html=True)
            counts = df['index_status'].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=counts.index.tolist(), values=counts.values.tolist(), hole=0.72,
                marker=dict(colors=["#3b82f6","#1a3060"], line=dict(color="#060d1f", width=3)),
                textfont=dict(family="Inter", size=12),
                hovertemplate="<b>%{label}</b><br>%{value} queries<extra></extra>",
            ))
            fig2.add_annotation(
                text=f"<b>{counts.get('Indexed',0)}</b><br><span style='font-size:10px'>INDEXED</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(family="JetBrains Mono", color="#3b82f6", size=20), align="center",
            )
            fig2.update_layout(**chart_layout(height=320, showlegend=True,
                legend=dict(orientation="h", y=-0.05, xanchor="center", x=0.5, font=dict(size=11))))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="sec-title">Latency Distribution</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Histogram(
            x=df["execution_time_ms"], nbinsx=35,
            marker=dict(color="#3b82f6", opacity=0.75, line=dict(color="#060d1f", width=0.3)),
            hovertemplate="<b>%{x:.0f} ms</b><br>Count: %{y}<extra></extra>",
        ))
        fig3.update_layout(**chart_layout(height=220,
            xaxis=dict(title="Execution Time (ms)", gridcolor="#0f1f3d"),
            yaxis=dict(title="Query Count",          gridcolor="#0f1f3d"),
            bargap=0.04))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    elif "Charts" in page:
        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown('<div class="sec-title">Complexity by Index Status</div>', unsafe_allow_html=True)
            fig4 = px.box(df, y="complexity_score", x="index_status", color="index_status",
                color_discrete_map={"Indexed":"#3b82f6","Non-Indexed":"#475569"},
                labels={"complexity_score":"Complexity Score","index_status":""}, points="all")
            fig4.update_traces(marker=dict(opacity=0.5, size=5))
            fig4.update_layout(**chart_layout(height=340, showlegend=False))
            st.plotly_chart(fig4, use_container_width=True)

        with c2:
            st.markdown('<div class="sec-title">Efficiency Distribution (Violin)</div>', unsafe_allow_html=True)
            fig5 = px.violin(df, y="efficiency_ratio", x="index_status", color="index_status", box=True,
                color_discrete_map={"Indexed":"#3b82f6","Non-Indexed":"#475569"},
                labels={"efficiency_ratio":"Efficiency Ratio","index_status":""})
            fig5.update_layout(**chart_layout(height=340, showlegend=False))
            st.plotly_chart(fig5, use_container_width=True)

        st.markdown('<div class="sec-title">Rows Examined vs Rows Returned</div>', unsafe_allow_html=True)
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(name="Rows Examined", x=display_df["id_x"].astype(str), y=display_df["rows_examined"], marker_color="#1a3060"))
        fig6.add_trace(go.Bar(name="Rows Returned", x=display_df["id_x"].astype(str), y=display_df["rows_returned"], marker_color="#3b82f6"))
        fig6.update_layout(**chart_layout(height=260, barmode="group",
            xaxis=dict(title="Query ID"), yaxis=dict(title="Row Count"),
            legend=dict(orientation="h", y=1.1, xanchor="right", x=1, font=dict(size=11))))
        st.plotly_chart(fig6, use_container_width=True)

    # ── Workload ──────────────────────────────────────────────────────────────
    elif "Workload" in page:
        c1, c2, c3 = st.columns(3, gap="large")

        with c1:
            st.markdown('<div class="sec-title">Top 10 Slowest Queries</div>', unsafe_allow_html=True)
            slowest = df.nlargest(10, "execution_time_ms")[["id_x","execution_time_ms"]].sort_values("execution_time_ms")
            fig7 = go.Figure(go.Bar(
                x=slowest["execution_time_ms"], y=slowest["id_x"].astype(str),
                orientation="h", marker_color="#3b82f6",
                hovertemplate="Query %{y}: %{x:.1f} ms<extra></extra>",
            ))
            fig7.update_layout(**chart_layout(height=340, xaxis=dict(title="ms"), yaxis=dict(title="Query ID")))
            st.plotly_chart(fig7, use_container_width=True)

        with c2:
            st.markdown('<div class="sec-title">Complexity vs Latency</div>', unsafe_allow_html=True)
            fig8 = px.scatter(df, x="complexity_score", y="execution_time_ms", color="index_status",
                color_discrete_map={"Indexed":"#3b82f6","Non-Indexed":"#475569"},
                labels={"complexity_score":"Complexity","execution_time_ms":"Latency (ms)"},
                trendline="ols")
            fig8.update_layout(**chart_layout(height=340, showlegend=True,
                legend=dict(orientation="h", y=1.08, font=dict(size=10))))
            st.plotly_chart(fig8, use_container_width=True)

        with c3:
            st.markdown('<div class="sec-title">Efficiency Histogram</div>', unsafe_allow_html=True)
            fig9 = go.Figure(go.Histogram(
                x=df["efficiency_ratio"], nbinsx=20,
                marker_color="#22c55e", opacity=0.75,
                hovertemplate="Efficiency %{x:.2f}: %{y} queries<extra></extra>",
            ))
            fig9.update_layout(**chart_layout(height=340,
                xaxis=dict(title="Efficiency Ratio"), yaxis=dict(title="Count"), bargap=0.04))
            st.plotly_chart(fig9, use_container_width=True)

    # ── Audit Log ─────────────────────────────────────────────────────────────
    elif "Audit" in page:
        s1, s2, s3, s4 = st.columns(4, gap="small")
        s1.metric("Showing",        f"{len(display_df)}")
        s2.metric("Max Latency",    f"{display_df['execution_time_ms'].max():.1f} ms")
        s3.metric("Min Latency",    f"{display_df['execution_time_ms'].min():.1f} ms")
        s4.metric("Avg Complexity", f"{display_df['complexity_score'].mean():.1f}")

        st.markdown("")
        st.markdown('<div class="sec-title">Full Query Audit</div>', unsafe_allow_html=True)
        st.dataframe(
            display_df[["id_x","sql_text","execution_time_ms","rows_examined","rows_returned","complexity_score","index_status","efficiency_ratio"]],
            column_config={
                "id_x":              st.column_config.NumberColumn("ID",           width="small"),
                "sql_text":          st.column_config.TextColumn("Query",          width="large"),
                "execution_time_ms": st.column_config.NumberColumn("Latency (ms)", format="%.1f ⚡"),
                "rows_examined":     st.column_config.NumberColumn("Rows Scanned", format="%d"),
                "rows_returned":     st.column_config.NumberColumn("Rows Sent",    format="%d"),
                "complexity_score":  st.column_config.NumberColumn("Complexity 🧩",format="%d"),
                "index_status":      st.column_config.TextColumn("Index"),
                "efficiency_ratio":  st.column_config.ProgressColumn("Efficiency", min_value=0, max_value=1, format="%.2f"),
            },
            hide_index=True, use_container_width=True, height=560,
        )

except Exception as e:
    st.error(f"⚠️  Failed to load data: {e}")
    st.info("Make sure `sql_dashboard/SQL_Performance_Analysis.csv` exists relative to this script.")
