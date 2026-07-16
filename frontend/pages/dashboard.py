import requests
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="AI Personal OS Dashboard",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 AI Personal OS Dashboard")

API = "http://127.0.0.1:8000"

# -----------------------------------------
# Sidebar
# -----------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Memory",
    ],
)

if page == "Dashboard":

    # -----------------------------------------
    # Dashboard Stats
    # -----------------------------------------

    response = requests.get(
        f"{API}/dashboard/stats"
    )

    if response.status_code != 200:

        st.error("Backend is not running.")

        st.stop()

    stats = response.json()

    # -----------------------------------------
    # Importance Distribution
    # -----------------------------------------

    importance_response = requests.get(
        f"{API}/dashboard/importance-distribution"
    )

    importance_distribution = {}

    if importance_response.status_code == 200:

        importance_distribution = (
            importance_response.json()
        )

    # -----------------------------------------
    # Top Memories
    # -----------------------------------------

    top_response = requests.get(
        f"{API}/dashboard/top-memories"
    )

    top_memories = []

    if top_response.status_code == 200:
        top_memories = top_response.json()

    # -----------------------------------------
    # Memory Timeline
    # -----------------------------------------

    timeline_response = requests.get(
        f"{API}/dashboard/memory-timeline"
    )

    timeline = {}

    if timeline_response.status_code == 200:

        timeline = timeline_response.json()

    # -----------------------------------------
    # Memory Health
    # -----------------------------------------

    health_response = requests.get(
        f"{API}/dashboard/memory-health"
    )

    health = {}

    if health_response.status_code == 200:

        health = health_response.json()

    # -----------------------------------------
    # Top Metrics
    # -----------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Memories",
            stats["total_memories"],
        )

    with col2:

        st.metric(
            "Average Importance",
            stats["avg_importance"],
        )

    # -----------------------------------------
    # Memory Health
    # -----------------------------------------

    if health:

        st.divider()

        st.subheader("🧠 Memory Health")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Health Score",
                f"{health['health_score']}%",
            )

        with col2:

            st.metric(
                "🟢 Active",
                health["active"],
            )

        with col3:

            st.metric(
                "🟡 Stale",
                health["stale"],
            )

        with col4:

            st.metric(
                "🔴 Never Used",
                health["never_used"],
            )

        st.progress(
            health["health_score"] / 100
        )

    # -----------------------------------------
    # Memory Types Pie Chart
    # -----------------------------------------

    st.divider()

    st.subheader("📊 Memory Types Distribution")

    memory_types = stats["memory_types"]

    if memory_types:

        fig = px.pie(
            names=list(memory_types.keys()),
            values=list(memory_types.values()),
            title="Memory Types",
        )

        # st.plotly_chart(
        #     fig,
        #     use_container_width=True,
        # )

    else:

        st.info("No memory types found.")

    # -----------------------------------------
    # Importance Distribution
    # -----------------------------------------

    st.divider()

    st.subheader("⭐ Importance Distribution")

    if importance_distribution:

        fig = px.bar(
            x=list(importance_distribution.keys()),
            y=list(importance_distribution.values()),
            labels={
                "x": "Importance",
                "y": "Memories",
            },
            title="Importance Levels",
            text=list(
                importance_distribution.values()
            ),
        )

        # st.plotly_chart(
        #     fig,
        #     use_container_width=True,
        # )

    else:

        st.info(
            "No importance data found."
        )

    # -----------------------------------------
    # Most Accessed Memory
    # -----------------------------------------

    st.divider()

    st.subheader("🔥 Most Accessed Memory")

    st.write(
        stats["most_accessed"]
    )

    # -----------------------------------------
    # Least Accessed Memory
    # -----------------------------------------

    st.divider()

    st.subheader("🧊 Least Accessed Memory")

    st.write(
        stats["least_accessed"]
    )

    # -----------------------------------------
    # Top Accessed Memories Bar Chart
    # -----------------------------------------

    st.divider()

    st.subheader("📈 Top Accessed Memories")

    if top_memories:

        fig = px.bar(
            top_memories,
            x="access_count",
            y="memory",
            orientation="h",
            title="Most Frequently Retrieved Memories",
            text="access_count",
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending",
            }
        )

        # st.plotly_chart(
        #     fig,
        #     use_container_width=True,
        # )

    else:

        st.info("No memories found.")

    # -----------------------------------------
    # Memory Explorer
    # -----------------------------------------

    st.divider()

    st.subheader("🗂 Memory Explorer")

    # -------------------------------------
    # Semantic Search
    # -------------------------------------

    search_query = st.text_input(
        "🔍 Semantic Search",
        placeholder="Ask anything about your memories...",
    )

    semantic_results = []

    if search_query:

        response = requests.get(
            f"{API}/memories/search",
            params={
                "session_id": "arnav",
                "query": search_query,
                "limit": 5,
            },
        )

        if response.status_code == 200:

            semantic_results = response.json()

        else:

            st.error("Semantic search failed.")

    # -------------------------------------
    # Search Results
    # -------------------------------------

    if semantic_results:

        st.success(
            f"Found {len(semantic_results)} similar memories"
        )

        for memory in semantic_results:

            with st.container(border=True):

                st.markdown(
                    f"### 🧠 {memory['memory']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.caption(
                        f"Type: {memory['memory_type']}"
                    )

                with col2:
                    st.caption(
                        f"Importance: {memory['importance']}"
                    )

                with col3:
                    st.caption(
                        f"Score: {memory['score']:.3f}"
                    )

    memory_response = requests.get(
        f"{API}/dashboard/memories"
    )

    if memory_response.status_code == 200:

        memories = memory_response.json()

        # -------------------------------------
        # Search + Filter
        # -------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            search = st.text_input(
                "🔍 Search Memory",
                placeholder="Search memories...",
            )

        with col2:

            memory_types = sorted(
                list(
                    {
                        memory["memory_type"]
                        for memory in memories
                    }
                )
            )

            selected_type = st.selectbox(
                "🏷 Memory Type",
                ["All"] + memory_types,
            )

        # -------------------------------------
        # Search Filter
        # -------------------------------------

        if search:

            memories = [
                memory
                for memory in memories
                if search.lower()
                in memory["memory"].lower()
            ]

        # -------------------------------------
        # Type Filter
        # -------------------------------------

        if selected_type != "All":

            memories = [
                memory
                for memory in memories
                if memory["memory_type"] == selected_type
            ]

        # -------------------------------------
        # Memory Table
        # -------------------------------------

        st.dataframe(
            memories,
            use_container_width=True,
            hide_index=True,
        )

        # -------------------------------------
        # Select Memory
        # -------------------------------------

        if memories:

            memory_options = {
                f"#{m['id']} | {m['memory']}": m
                for m in memories
            }

            selected_label = st.selectbox(
                "Select Memory",
                options=list(memory_options.keys()),
            )

            selected_memory = memory_options[selected_label]

            st.write(selected_memory)

            # -------------------------------------
            # Edit Memory
            # -------------------------------------

            st.divider()
            st.subheader("✏️ Edit Selected Memory")

            edited_memory = st.text_area(
                "Memory",
                value=selected_memory["memory"],
                key=f"memory_{selected_memory['id']}",
            )

            st.write(edited_memory)

            edited_type = st.selectbox(
                "Memory Type",
                [
                    "fact",
                    "preference",
                    "goal",
                    "project",
                    "identity",
                    "skill",
                ],
                index=[
                    "fact",
                    "preference",
                    "goal",
                    "project",
                    "identity",
                    "skill",
                ].index(selected_memory["memory_type"]),
                key=f"type_{selected_memory['id']}",
            )

            st.write(edited_type)

            edited_importance = st.number_input(
                "Importance",
                min_value=1,
                max_value=10,
                value=int(selected_memory["importance"]),
                step=1,
                key=f"importance_{selected_memory['id']}",
            )

            st.write(edited_importance)

            if st.button(
                "💾 Update Memory",
                type="primary",
            ):

                payload = {
                    "session_id": "arnav",
                    "memory": edited_memory,
                    "memory_type": edited_type,
                    "importance": edited_importance,
                }

                response = requests.put(
                    f"{API}/memories/{selected_memory['id']}",
                    json=payload,
                )

                if response.status_code == 200:

                    st.success(
                        "✅ Memory updated successfully."
                    )

                    # st.rerun()

                else:

                    st.error(
                        response.text
                    )

            # -------------------------------------
            # Delete Memory
            # -------------------------------------

            if st.button(
                "🗑 Delete Selected Memory",
                type="secondary",
            ):

                response = requests.delete(
                    f"{API}/memories/{selected_memory['id']}"
                )

                if response.status_code == 200:

                    st.success(
                        "✅ Memory deleted successfully."
                    )

                    # st.rerun()

                else:

                    st.error(
                        response.text
                    )

    else:

        st.error(
            "Unable to load memories."
        )

    # -----------------------------------------
    # Memory Timeline
    # -----------------------------------------

    st.divider()

    st.subheader("📅 Memory Timeline")

    if timeline:

        fig = px.line(
            x=list(timeline.keys()),
            y=list(timeline.values()),
            markers=True,
            labels={
                "x": "Date",
                "y": "Memories Created",
            },
            title="Memory Growth Over Time",
        )

        # st.plotly_chart(
        #     fig,
        #     use_container_width=True,
        # )

    else:

        st.info(
            "No timeline data found."
        )

    # -----------------------------------------
    # AI Reflection
    # -----------------------------------------

    st.divider()

    st.subheader("🤖 AI Reflection")

    col1, col2 = st.columns([1, 4])

    with col1:

        if st.button(
            "Generate Reflection",
            type="primary",
        ):

            requests.get(
                f"{API}/memories/reflection"
            )

            st.rerun()

    # -----------------------------------------
    # Reflection History
    # -----------------------------------------

    history_response = requests.get(
        f"{API}/memories/reflections"
    )

    if history_response.status_code == 200:

        reflections = history_response.json()

        if reflections:

            latest = reflections[0]

            st.success(
                latest["reflection"],
                icon="🧠",
            )

            st.divider()

            st.subheader("📚 Reflection History")

            for reflection in reflections:

                stars = "⭐" * reflection["importance"]

                with st.expander(
                    f"{reflection['created_at']}   {stars}"
                ):

                    st.write(
                        reflection["reflection"]
                    )

        else:

            st.info(
                "No reflections available."
            )

    else:

        st.error(
            "Unable to load reflections."
        )

# -----------------------------------------
# Add Memory
# -----------------------------------------

if page == "Add Memory":

    st.title("➕ Add New Memory")

    memory = st.text_area(
        "Memory",
        placeholder="Enter a memory...",
    )

    memory_type = st.selectbox(
        "Memory Type",
        [
            "fact",
            "preference",
            "goal",
            "project",
            "identity",
            "skill",
        ],
    )

    importance = st.slider(
        "Importance",
        min_value=1,
        max_value=10,
        value=5,
    )

    save = st.button(
        "💾 Save Memory",
        type="primary",
    )

    if save:

        payload = {
            "session_id": "arnav",
            "memory": memory,
            "memory_type": memory_type,
            "importance": importance,
        }

        response = requests.post(
            f"{API}/memories/",
            json=payload,
        )

        if response.status_code == 200:

            st.success("✅ Memory Saved Successfully!")

            # st.rerun()

        else:

            st.error(
                f"❌ Error: {response.text}"
            )