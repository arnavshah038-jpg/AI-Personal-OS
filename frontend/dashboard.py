import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =====================================================================
# CONFIG
# =====================================================================

st.set_page_config(
    page_title="AI Personal OS",
    page_icon="🧠",
    layout="wide",
)

API = "http://backend:8000"

# ---------------------------------------------------------------------
# Design tokens — "Memory Pulse" identity
# Deep indigo night backdrop (the "mind"), amber sparks for importance/
# energy, teal for health/active signal, coral for stale/at-risk.
# ---------------------------------------------------------------------

BG = "#10122A"
PANEL = "#191C3D"
PANEL_2 = "#20244C"
BORDER = "#31356A"
TEXT = "#EDEDF7"
MUTED = "#9797B8"
AMBER = "#F2A65A"
TEAL = "#5EEAD4"
CORAL = "#F27C6B"
VIOLET = "#A78BFA"

CHART_COLORWAY = [AMBER, TEAL, VIOLET, CORAL]


# =====================================================================
# STYLE INJECTION
# =====================================================================

def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 15% 0%, #1A1D46 0%, transparent 45%),
                radial-gradient(circle at 100% 30%, #171A3E 0%, transparent 50%),
                {BG};
            color: {TEXT};
        }}

        section[data-testid="stSidebar"] {{
            background: #0D0E24;
            border-right: 1px solid {BORDER};
        }}

        h1, h2, h3 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: {TEXT} !important;
            letter-spacing: -0.01em;
        }}

        p, span, label, div {{
            color: {TEXT};
        }}

        /* Eyebrow / section label */
        .eyebrow {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: {AMBER};
            margin: 4px 0 2px 0;
        }}
        .eyebrow::before {{
            content: "";
            width: 6px; height: 6px; border-radius: 50%;
            background: {AMBER};
            box-shadow: 0 0 8px {AMBER};
        }}

        /* Header banner */
        .hero {{
            padding: 22px 26px;
            border-radius: 16px;
            background: linear-gradient(120deg, #1B1E48 0%, #171A3A 100%);
            border: 1px solid {BORDER};
            margin-bottom: 18px;
        }}
        .hero h1 {{
            font-size: 30px !important;
            margin: 4px 0 2px 0 !important;
        }}
        .hero p {{
            color: {MUTED};
            font-size: 14px;
            margin: 0;
        }}

        /* Custom metric card */
        .metric-card {{
            background: {PANEL};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 16px 18px;
            height: 100%;
        }}
        .metric-card .m-label {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11.5px;
            color: {MUTED};
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .metric-card .m-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin-top: 4px;
        }}
        .metric-card .m-icon {{
            font-size: 20px;
            opacity: 0.9;
        }}

        /* Chip row for health status */
        .chip {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 999px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12.5px;
            border: 1px solid {BORDER};
            background: {PANEL_2};
            margin-right: 8px;
        }}

        /* Panels wrapping charts / tables */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {PANEL};
            border: 1px solid {BORDER} !important;
            border-radius: 14px;
        }}

        hr {{
            border-color: {BORDER} !important;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 14.5px;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: {AMBER} !important;
        }}

        /* Inputs */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background: {PANEL_2} !important;
            color: {TEXT} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 8px !important;
        }}

        /* Buttons */
        .stButton button {{
            border-radius: 9px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            border: 1px solid {BORDER};
        }}
        .stButton button[kind="primary"] {{
            background: {AMBER};
            color: #10122A;
            border: none;
        }}

        /* Dataframe */
        [data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: 10px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon: str, label: str, value, accent: str = TEXT):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="m-icon">{icon}</div>
            <div class="m-label">{label}</div>
            <div class="m-value" style="color:{accent};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_chart_theme(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT, size=12.5),
        title_font=dict(family="Space Grotesk, sans-serif", size=15, color=TEXT),
        margin=dict(l=10, r=10, t=48, b=10),
        height=height,
        colorway=CHART_COLORWAY,
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def health_gauge(score: float):
    """Signature element: the Memory Pulse — a circular health gauge."""
    color = TEAL if score >= 70 else (AMBER if score >= 40 else CORAL)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 30, "color": TEXT, "family": "Space Grotesk"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": MUTED, "tickfont": {"color": MUTED, "size": 10}},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": PANEL_2,
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(242,124,107,0.12)"},
                    {"range": [40, 70], "color": "rgba(242,166,90,0.12)"},
                    {"range": [70, 100], "color": "rgba(94,234,212,0.12)"},
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        height=200,
        margin=dict(l=20, r=20, t=10, b=10),
    )
    return fig


inject_css()

# =====================================================================
# SIDEBAR NAVIGATION  (same two destinations as before)
# =====================================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:6px 2px 18px 2px;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size:20px; font-weight:700;">
                🧠 AI Personal OS
            </div>
            <div style="color:{MUTED}; font-size:12px; font-family:'IBM Plex Mono',monospace;">
                memory-augmented assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["Dashboard", "Add Memory"],
        label_visibility="collapsed",
    )

# =====================================================================
# DASHBOARD PAGE
# =====================================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Live session · arnav</div>
            <h1>🧠 Memory Control Center</h1>
            <p>How much your assistant remembers, what it trusts most, and how it's holding up over time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # Fetch all dashboard data (same endpoints)
    # -----------------------------------------

    response = requests.get(f"{API}/dashboard/stats")

    if response.status_code != 200:
        st.error("Backend is not running.")
        st.stop()

    stats = response.json()

    importance_response = requests.get(f"{API}/dashboard/importance-distribution")
    importance_distribution = importance_response.json() if importance_response.status_code == 200 else {}

    top_response = requests.get(f"{API}/dashboard/top-memories")
    top_memories = top_response.json() if top_response.status_code == 200 else []

    timeline_response = requests.get(f"{API}/dashboard/memory-timeline")
    timeline = timeline_response.json() if timeline_response.status_code == 200 else {}

    health_response = requests.get(f"{API}/dashboard/memory-health")
    health = health_response.json() if health_response.status_code == 200 else {}

    tab_overview, tab_analytics, tab_explorer, tab_reflection = st.tabs(
        ["🧭 Overview", "📊 Analytics", "🗂 Explorer", "🤖 Reflections"]
    )

    # =================================================================
    # TAB — OVERVIEW
    # =================================================================
    with tab_overview:

        col1, col2 = st.columns(2)
        with col1:
            metric_card("📚", "Total Memories", stats["total_memories"], AMBER)
        with col2:
            metric_card("⭐", "Average Importance", stats["avg_importance"], AMBER)

        if health:
            st.markdown("<div class='eyebrow' style='margin-top:22px;'>Memory Pulse</div>", unsafe_allow_html=True)

            gcol, ccol = st.columns([1, 1.4])

            with gcol:
                st.plotly_chart(
                    apply_chart_theme(health_gauge(health["health_score"]), height=210),
                    width="stretch",
                    config={"displayModeBar": False},
                )

            with ccol:
                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <span class="chip">🟢 Active&nbsp;&nbsp;<b>{health['active']}</b></span>
                    <span class="chip">🟡 Stale&nbsp;&nbsp;<b>{health['stale']}</b></span>
                    <span class="chip">🔴 Never used&nbsp;&nbsp;<b>{health['never_used']}</b></span>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
                st.caption("Health score weighs recently-active memories and overall engagement.")

        st.markdown("<div class='eyebrow' style='margin-top:22px;'>Access extremes</div>", unsafe_allow_html=True)
        acol, lcol = st.columns(2)
        with acol:
            with st.container(border=True):
                st.markdown("**🔥 Most accessed memory**")
                st.write(stats["most_accessed"])
        with lcol:
            with st.container(border=True):
                st.markdown("**🧊 Least accessed memory**")
                st.write(stats["least_accessed"])

    # =================================================================
    # TAB — ANALYTICS
    # =================================================================
    with tab_analytics:

        row1_a, row1_b = st.columns(2)

        with row1_a:
            st.markdown("<div class='eyebrow'>Memory types</div>", unsafe_allow_html=True)
            memory_types = stats["memory_types"]
            if memory_types:
                fig = px.bar(
                    x=list(memory_types.keys()),
                    y=list(memory_types.values()),
                    labels={"x": "Memory Type", "y": "Count"},
                )
                fig.update_traces(marker_color=AMBER)
                st.plotly_chart(apply_chart_theme(fig), width="stretch")
            else:
                st.info("No memory types found.")

        with row1_b:
            st.markdown("<div class='eyebrow'>Importance distribution</div>", unsafe_allow_html=True)
            if importance_distribution:
                fig = px.bar(
                    x=list(importance_distribution.keys()),
                    y=list(importance_distribution.values()),
                    labels={"x": "Importance", "y": "Memories"},
                    text=list(importance_distribution.values()),
                )
                fig.update_traces(marker_color=TEAL)
                st.plotly_chart(apply_chart_theme(fig), width="stretch")
            else:
                st.info("No importance data found.")

        row2_a, row2_b = st.columns(2)

        with row2_a:
            st.markdown("<div class='eyebrow'>Top accessed memories</div>", unsafe_allow_html=True)
            if top_memories:
                fig = px.bar(
                    top_memories,
                    x="access_count",
                    y="memory",
                    orientation="h",
                    text="access_count",
                )
                fig.update_traces(marker_color=VIOLET)
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(apply_chart_theme(fig), width="stretch")
            else:
                st.info("No memories found.")

        with row2_b:
            st.markdown("<div class='eyebrow'>Memory growth over time</div>", unsafe_allow_html=True)
            if timeline:
                fig = px.line(
                    x=list(timeline.keys()),
                    y=list(timeline.values()),
                    markers=True,
                    labels={"x": "Date", "y": "Memories Created"},
                )
                fig.update_traces(line_color=TEAL, marker=dict(color=AMBER, size=8))
                st.plotly_chart(apply_chart_theme(fig), width="stretch")
            else:
                st.info("No timeline data found.")

    # =================================================================
    # TAB — EXPLORER  (semantic search + table + edit/delete)
    # =================================================================
    with tab_explorer:

        st.markdown("<div class='eyebrow'>Semantic search</div>", unsafe_allow_html=True)

        search_query = st.text_input(
            "🔍 Semantic Search",
            placeholder="Ask anything about your memories...",
            label_visibility="collapsed",
        )

        semantic_results = []

        if search_query:
            response = requests.get(
                f"{API}/memories/search",
                params={"session_id": "arnav", "query": search_query, "limit": 5},
            )
            if response.status_code == 200:
                semantic_results = response.json()
            else:
                st.error("Semantic search failed.")

        if semantic_results:
            st.success(f"Found {len(semantic_results)} similar memories")

            for memory in semantic_results:
                with st.container(border=True):
                    st.markdown(f"### 🧠 {memory['memory']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"Type: {memory['memory_type']}")
                    with col2:
                        st.caption(f"Importance: {memory['importance']}")
                    with col3:
                        st.caption(f"Score: {memory['score']:.3f}")

        st.markdown("<div class='eyebrow' style='margin-top:20px;'>All memories</div>", unsafe_allow_html=True)

        memory_response = requests.get(f"{API}/dashboard/memories")

        if memory_response.status_code == 200:

            memories = memory_response.json()

            col1, col2 = st.columns(2)
            with col1:
                search = st.text_input("🔍 Search Memory", placeholder="Search memories...")
            with col2:
                memory_types = sorted(list({memory["memory_type"] for memory in memories}))
                selected_type = st.selectbox("🏷 Memory Type", ["All"] + memory_types)

            if search:
                memories = [m for m in memories if search.lower() in m["memory"].lower()]

            if selected_type != "All":
                memories = [m for m in memories if m["memory_type"] == selected_type]

            st.dataframe(memories, width="stretch", hide_index=True)

            if memories:
                memory_options = {f"#{m['id']} | {m['memory']}": m for m in memories}
                selected_label = st.selectbox("Select Memory", options=list(memory_options.keys()))
                selected_memory = memory_options[selected_label]

                st.markdown("<div class='eyebrow' style='margin-top:16px;'>Edit selected memory</div>", unsafe_allow_html=True)

                edited_memory = st.text_area(
                    "Memory",
                    value=selected_memory["memory"],
                    key=f"memory_{selected_memory['id']}",
                )

                edited_type = st.selectbox(
                    "Memory Type",
                    ["fact", "preference", "goal", "project", "identity", "skill"],
                    index=["fact", "preference", "goal", "project", "identity", "skill"].index(
                        selected_memory["memory_type"]
                    ),
                    key=f"type_{selected_memory['id']}",
                )

                edited_importance = st.number_input(
                    "Importance",
                    min_value=1,
                    max_value=10,
                    value=int(selected_memory["importance"]),
                    step=1,
                    key=f"importance_{selected_memory['id']}",
                )

                bcol1, bcol2 = st.columns(2)

                with bcol1:
                    if st.button("💾 Update Memory", type="primary", width="stretch"):
                        payload = {
                            "session_id": "arnav",
                            "memory": edited_memory,
                            "memory_type": edited_type,
                            "importance": edited_importance,
                        }
                        response = requests.put(f"{API}/memories/{selected_memory['id']}", json=payload)
                        if response.status_code == 200:
                            st.success("✅ Memory updated successfully.")
                        else:
                            st.error(response.text)

                with bcol2:
                    if st.button("🗑 Delete Selected Memory", type="secondary", width="stretch"):
                        response = requests.delete(f"{API}/memories/{selected_memory['id']}")
                        if response.status_code == 200:
                            st.success("✅ Memory deleted successfully.")
                        else:
                            st.error(response.text)
        else:
            st.error("Unable to load memories.")

    # =================================================================
    # TAB — REFLECTIONS
    # =================================================================
    with tab_reflection:

        st.markdown("<div class='eyebrow'>AI reflection</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✨ Generate Reflection", type="primary", width="stretch"):
                requests.get(f"{API}/memories/reflection")
                st.rerun()

        history_response = requests.get(f"{API}/memories/reflections")

        if history_response.status_code == 200:
            reflections = history_response.json()

            if reflections:
                latest = reflections[0]
                st.success(latest["reflection"], icon="🧠")

                st.markdown("<div class='eyebrow' style='margin-top:18px;'>Reflection history</div>", unsafe_allow_html=True)

                for reflection in reflections:
                    stars = "⭐" * reflection["importance"]
                    with st.expander(f"{reflection['created_at']}   {stars}"):
                        st.write(reflection["reflection"])
            else:
                st.info("No reflections available.")
        else:
            st.error("Unable to load reflections.")

# =====================================================================
# ADD MEMORY PAGE
# =====================================================================

if page == "Add Memory":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">New entry</div>
            <h1>➕ Add a Memory</h1>
            <p>Manually teach the assistant something it should remember.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    memory = st.text_area("Memory", placeholder="Enter a memory...")

    memory_type = st.selectbox(
        "Memory Type",
        ["fact", "preference", "goal", "project", "identity", "skill"],
    )

    importance = st.slider("Importance", min_value=1, max_value=10, value=5)

    save = st.button("💾 Save Memory", type="primary")

    if save:
        payload = {
            "session_id": "arnav",
            "memory": memory,
            "memory_type": memory_type,
            "importance": importance,
        }
        response = requests.post(f"{API}/memories/", json=payload)

        if response.status_code == 200:
            st.success("✅ Memory Saved Successfully!")
        else:
            st.error(f"❌ Error: {response.text}")
