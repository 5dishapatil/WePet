"""
styles.py — Global CSS for WePet MVP.
Aesthetic: Dark luxury / refined product feel.
"""

RISK_COLORS = {
    "Low": "#22c55e",
    "Moderate": "#f59e0b",
    "High": "#f97316",
    "Critical": "#ef4444",
}

RISK_BG = {
    "Low": "rgba(34, 197, 94, 0.12)",
    "Moderate": "rgba(245, 158, 11, 0.12)",
    "High": "rgba(249, 115, 22, 0.12)",
    "Critical": "rgba(239, 68, 68, 0.12)",
}


def get_global_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ─── Base Reset ────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

/* ─── Hide default Streamlit chrome ────────────────────────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* ─── Sidebar ───────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #13161e !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
    font-size: 0.82rem;
}

/* ─── Sidebar navigation buttons ───────────────────────────────────────── */
.nav-button {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border-radius: 10px;
    cursor: pointer;
    margin-bottom: 6px;
    transition: all 0.2s;
    border: 1px solid transparent;
    font-size: 0.93rem;
    font-weight: 500;
    color: #94a3b8;
    background: transparent;
    width: 100%;
    text-align: left;
}
.nav-button:hover {
    background: rgba(255,255,255,0.05);
    color: #e2e8f0;
    border-color: rgba(255,255,255,0.08);
}
.nav-button.active {
    background: rgba(99, 179, 237, 0.12);
    color: #63b3ed;
    border-color: rgba(99, 179, 237, 0.25);
}

/* ─── Headers ───────────────────────────────────────────────────────────── */
h1, h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

/* ─── Cards ─────────────────────────────────────────────────────────────── */
.pt-card {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.pt-card-sm {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

/* ─── Risk Badge ─────────────────────────────────────────────────────────── */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ─── Score Meter ────────────────────────────────────────────────────────── */
.score-bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
    height: 6px;
    overflow: hidden;
    margin-top: 6px;
}
.score-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}

/* ─── Metric Cards ───────────────────────────────────────────────────────── */
.metric-card {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 14px;
    text-align: center;
}
.metric-value {
    font-size: 1.7rem;
    font-weight: 700;
    line-height: 1.1;
    color: #f1f5f9;
}
.metric-label {
    font-size: 0.74rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}
.metric-unit {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 400;
}

/* ─── Tag chips ─────────────────────────────────────────────────────────── */
.chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.77rem;
    font-weight: 500;
    margin: 2px;
    background: rgba(255,255,255,0.06);
    color: #94a3b8;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ─── Dividers ───────────────────────────────────────────────────────────── */
.pt-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 20px 0;
}

/* ─── Streamlit button overrides ─────────────────────────────────────────── */
.stButton > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px) !important;
}

/* ─── Success button ─────────────────────────────────────────────────────── */
.stButton > button[kind="secondary"] {
    background: rgba(34,197,94,0.15) !important;
    color: #22c55e !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
}

/* ─── Inputs ─────────────────────────────────────────────────────────────── */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: #1e2230 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ─── Checkbox ───────────────────────────────────────────────────────────── */
.stCheckbox > label {
    color: #94a3b8 !important;
    font-size: 0.9rem !important;
}

/* ─── Sub-score grid ─────────────────────────────────────────────────────── */
.sub-score-card {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    height: 100%;
}
.sub-score-title {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #64748b;
    margin-bottom: 6px;
    font-weight: 600;
}
.sub-score-value {
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1;
}

/* ─── Driver cards ───────────────────────────────────────────────────────── */
.driver-card {
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #e2e8f0;
    line-height: 1.5;
}

/* ─── Rec cards ─────────────────────────────────────────────────────────── */
.rec-card {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #2563eb;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.rec-category {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #4d80e6;
    font-weight: 600;
    margin-bottom: 5px;
}
.rec-advice {
    font-size: 0.9rem;
    color: #e2e8f0;
    line-height: 1.5;
    margin-bottom: 6px;
}
.rec-why {
    font-size: 0.8rem;
    color: #64748b;
    font-style: italic;
}

/* ─── Emergency card ─────────────────────────────────────────────────────── */
.emergency-card {
    background: rgba(239, 68, 68, 0.06);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 12px;
    padding: 18px 20px;
}
.warning-sign {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.82rem;
    color: #fca5a5;
    margin: 3px;
}

/* ─── Window cards ───────────────────────────────────────────────────────── */
.window-card {
    background: rgba(34, 197, 94, 0.06);
    border: 1px solid rgba(34, 197, 94, 0.15);
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}
.window-time {
    font-size: 1.3rem;
    font-weight: 700;
    color: #4ade80;
    font-family: 'DM Mono', monospace;
}

/* ─── Exposure card ─────────────────────────────────────────────────────── */
.exposure-card {
    background: rgba(99, 179, 237, 0.06);
    border: 1px solid rgba(99, 179, 237, 0.15);
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}
.exposure-label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #90cdf4;
}

/* ─── Community cards ────────────────────────────────────────────────────── */
.task-card {
    background: linear-gradient(135deg, #1a2035 0%, #1e2840 100%);
    border: 1px solid rgba(99, 179, 237, 0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.points-badge {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #fbbf24;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
}

/* ─── NGO Report Cards ───────────────────────────────────────────────────── */
.report-card {
    background: #181c26;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
}

/* ─── Logo text ─────────────────────────────────────────────────────────── */
.logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #f1f5f9;
}
.logo-accent {
    color: #3b82f6;
}
.logo-sub {
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ─── Page header ────────────────────────────────────────────────────────── */
.page-header {
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    margin: 0;
}
.page-subtitle {
    font-size: 0.88rem;
    color: #64748b;
    margin-top: 4px;
}

/* ─── Section labels ─────────────────────────────────────────────────────── */
.section-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    font-weight: 600;
    margin-bottom: 10px;
    margin-top: 24px;
}

/* ─── Info chip ─────────────────────────────────────────────────────────── */
.info-chip {
    background: rgba(99, 179, 237, 0.1);
    border: 1px solid rgba(99, 179, 237, 0.2);
    color: #90cdf4;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 500;
    display: inline-block;
}

/* ─── Scrollbars ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
</style>
"""