"""
app.py — WePet MVP main entry point.
Run with: streamlit run app.py
"""
import streamlit as st

# ── Page Config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="WePet — Climate Risk Intelligence",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Apply Global Styles ────────────────────────────────────────────────────────
from components.styles import get_global_css
from components.ui import render_logo

st.markdown(get_global_css(), unsafe_allow_html=True)

# Hide Streamlit's auto-generated multipage nav (pages/ folder detection)
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Navigation State ───────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Pet Owner"

PAGES = {
    "🐾 Pet Owner": "Pet Owner",
    "🤝 Community": "Community",
    "🏥 NGO / Shelter": "NGO",
}

PAGE_DESCRIPTIONS = {
    "Pet Owner": "Real-time breed-specific risk analysis",
    "Community": "Daily 1-min task to help street animals",
    "NGO / Shelter": "Distress reports & severity dashboard",
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    render_logo()

    st.markdown(
        '<div class="section-label">MODE</div>',
        unsafe_allow_html=True,
    )

    for label, key in PAGES.items():
        is_active = st.session_state.page == key
        active_class = "nav-button active" if is_active else "nav-button"
        # Use button — clicking triggers rerun and updates state
        if st.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
            help=PAGE_DESCRIPTIONS.get(key, ""),
        ):
            st.session_state.page = key
            # Clear stale page-specific results when switching modes
            for k in ["pet_results", "comm_data", "ngo_last_report"]:
                st.session_state.pop(k, None)
            st.rerun()

    st.markdown("<hr class='pt-divider'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:0.75rem;color:#334155;line-height:1.6;padding:4px 0;">
            <strong style="color:#475569;">WePet</strong> is a climate risk
            intelligence tool for pets and street animals.<br><br>
            Weather data: Open-Meteo (free, no key).<br>
            All risk logic is deterministic and breed-specific.<br><br>
            <span style="color:#1e293b;">Not a veterinary service.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Page Router ────────────────────────────────────────────────────────────────
current_page = st.session_state.get("page", "Pet Owner")

try:
    if current_page == "Pet Owner":
        from pages.pet_owner import render as render_pet_owner
        render_pet_owner()

    elif current_page == "Community":
        from pages.community import render as render_community
        render_community()

    elif current_page == "NGO":
        from pages.ngo import render as render_ngo
        render_ngo()

    else:
        st.markdown(
            """
            <div style="text-align:center;padding:80px 20px;color:#475569;">
                Page not found. Use the sidebar to navigate.
            </div>
            """,
            unsafe_allow_html=True,
        )

except ImportError as e:
    st.error(f"Failed to load page module: {e}")
    st.markdown(
        """
        <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);
             border-radius:10px;padding:16px 20px;font-size:0.86rem;color:#fca5a5;">
            ❌ A required module could not be imported. Check that all
            <code>services/</code> and <code>components/</code> files are present.
        </div>
        """,
        unsafe_allow_html=True,
    )
except Exception as e:
    st.error(f"Unexpected error: {e}")
    raise