import streamlit as st
import os
import pandas as pd

from vision_module.vision_core import run_vision
from orchestrator.aura_core import main as run_audio

st.set_page_config(page_title="AURA System", layout="wide")

# =========================
# FIXED RESPONSIVE UI
# =========================
st.markdown("""
<style>

/* Let Streamlit handle responsiveness naturally */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

/* Make charts fully responsive */
[data-testid="stPlotlyChart"] {
    width: 100% !important;
}

/* Make tables responsive */
[data-testid="stDataFrame"] {
    width: 100% !important;
}

/* Prevent horizontal scroll */
html, body {
    overflow-x: hidden;
}

/* Better spacing */
section.main > div {
    padding-left: 1rem;
    padding-right: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("AURA: REAL TIME AUDITORY SCENE AND SOCIAL CONTEXUlIZER")
st.markdown("A system that understands the environment using multiple perception layers.")

# =========================
# SIDEBAR MODE
# =========================
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Audio Analysis (Real-Time)", "Vision Analysis (Video)"]
)

# =========================
# AUDIO MODE
# =========================
if mode == "Audio Analysis (Real-Time)":

    st.header("Audio Environment Analysis")

    st.sidebar.subheader("Audio Controls")
    duration = st.sidebar.slider("Recording Duration (seconds)", 5, 60, 30)

    show_conf = st.sidebar.checkbox("Confidence Trend", True)
    show_dist = st.sidebar.checkbox("Environment Distribution", True)
    show_vad = st.sidebar.checkbox("VAD Activity", False)

    if st.button("Start Analysis"):

        with st.spinner("Analyzing..."):
            run_audio(duration)

        st.success("Analysis completed")

        log_path = "logs/aura_logs.csv"

        if os.path.exists(log_path):
            df = pd.read_csv(log_path)

            st.subheader("Log Data")
            st.dataframe(df)

            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Confidence", round(df["confidence"].mean(), 2))
            col2.metric("Dominant Label", df["label"].mode()[0])
            col3.metric("Total Frames", len(df))

            if show_conf:
                st.subheader("Confidence Trend")
                st.line_chart(df["confidence"])

            if show_dist:
                st.subheader("Environment Distribution")
                st.bar_chart(df["label"].value_counts())

            if show_vad:
                st.subheader("VAD Activity")
                st.line_chart(df["vad"].astype(int))

# =========================
# VISION MODE
# =========================
elif mode == "Vision Analysis (Video)":

    st.header("Vision Environment Analysis")

    st.sidebar.subheader("Analysis Controls")

    show_activity = st.sidebar.checkbox("Scene Activity Flow", True)
    show_motion = st.sidebar.checkbox("Motion Intensity", True)
    show_spikes = st.sidebar.checkbox("Event Spikes", True)
    show_env = st.sidebar.checkbox("Environment Transition", True)

    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if uploaded_file:

        temp_path = "temp_video.mp4"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        st.video(temp_path)

        if st.button("Run Analysis"):

            with st.spinner("Processing..."):
                summary, df = run_vision(temp_path)

            st.success("Analysis completed")

            st.subheader("Scene Interpretation")
            st.write(summary)

            if os.path.exists("output.mp3"):
                st.audio("output.mp3")

            if df is not None and not df.empty:

                st.subheader("Detection Data")
                st.dataframe(df)

                # =========================
                # SYSTEM INTERPRETATION
                # =========================
                st.subheader("System Interpretation")

                avg_conf = df["confidence"].mean()

                if avg_conf > 0.75:
                    confidence_label = "High"
                elif avg_conf > 0.5:
                    confidence_label = "Moderate"
                else:
                    confidence_label = "Low"

                dominant_env = df["environment"].mode()[0]

                activity = (df["people"] + df["animals"] + df["vehicles"]).mean()

                if activity > 5:
                    activity_level = "High activity"
                elif activity > 2:
                    activity_level = "Moderate activity"
                else:
                    activity_level = "Low activity"

                st.markdown(f"""
                **Final Conclusion**

                The system identifies a **{dominant_env} environment** with  
                **{activity_level}** and **{confidence_label} confidence stability**.
                """)

                if confidence_label == "High":
                    st.success(f"System Confidence: {confidence_label}")
                elif confidence_label == "Moderate":
                    st.warning(f"System Confidence: {confidence_label}")
                else:
                    st.error(f"System Confidence: {confidence_label}")

                # =========================
                # BEHAVIORAL ANALYSIS
                # =========================
                st.subheader("Behavioral Analysis")

                if len(df) > 2:

                    df["activity"] = df["people"] + df["animals"] + df["vehicles"]
                    df["activity_change"] = df["activity"].diff().fillna(0)

                    if show_activity:
                        st.markdown("Scene Activity Change")
                        st.line_chart(df["activity_change"])

                    if show_motion:
                        st.markdown("Motion Intensity")

                        motion_map = {
                            "none": 0,
                            "steady": 1,
                            "approaching": 2,
                            "moving": 2
                        }

                        df["motion_score"] = df.get("motion", "").map(motion_map).fillna(0)
                        st.area_chart(df["motion_score"])

                    if show_spikes:
                        st.markdown("Event Spikes")

                        spikes = df.index[abs(df["activity_change"]) > 2]

                        if len(spikes) > 0:
                            spike_df = df.loc[spikes]
                            st.scatter_chart(
                                spike_df[["activity"]].reset_index(),
                                x="index",
                                y="activity"
                            )
                        else:
                            st.info("No major activity spikes detected.")

                    if show_env and "environment" in df.columns:
                        st.markdown("Environment Transition")

                        env_map = {e: i for i, e in enumerate(df["environment"].unique())}
                        df["env_encoded"] = df["environment"].map(env_map)

                        st.line_chart(df["env_encoded"])

                else:
                    st.warning("Not enough data for analysis.")