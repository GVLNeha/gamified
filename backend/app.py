import streamlit as st
import pandas as pd
from modules import utils, gamification, nudges
import os

# ----------------------------
# 0. Paths for frontend assets
# ----------------------------
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')
CSS_PATH = os.path.join(BASE_DIR, 'styles', 'custom.css')
ICON_LIGHT = os.path.join(BASE_DIR, 'icons', 'icon-light-32x32.png')
ICON_DARK = os.path.join(BASE_DIR, 'icons', 'icon-dark-32x32.png')
APPLE_ICON = os.path.join(BASE_DIR, 'icons', 'apple-icon.png')

# ----------------------------
# 1. Page Config
# ----------------------------
st.set_page_config(
    page_title="Gamified Performance Feedback Agent",
    page_icon="🎮",
    layout="wide"
)

# ----------------------------
# 2. Load frontend CSS
# ----------------------------
if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------
# 3. Title
# ----------------------------
st.title("🎮 Gamified Performance Feedback Agent")
st.markdown("Transform monthly KPIs into points, levels, badges, nudges, and interactive feedback!")

# ----------------------------
# 4. Upload KPI Data
# ----------------------------
st.sidebar.header("Upload KPI Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=['csv','xlsx'])

if uploaded_file:
    # Load and process
    df = utils.load_kpi_data(uploaded_file)
    df = utils.clean_data(df)
    df = gamification.gamify(df)
    df = nudges.add_nudges(df)

    # ----------------------------
    # 5. Live Tracking
    # ----------------------------
    st.subheader("📊 Live Tracking")
    total_employees = len(df)
    avg_points = int(df['points'].mean())
    top_employee = df.loc[df['points'].idxmax()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", total_employees)
    col2.metric("Average Score", avg_points)
    col3.metric("Top Performer", f"{top_employee['employee_name']} ({int(top_employee['points'])} pts)")

    # ----------------------------
    # 6. Top 3 Leaderboard
    # ----------------------------
    st.subheader("🏆 Top Performers")
    top3 = df.sort_values('points', ascending=False).head(3).reset_index(drop=True)
    medals = ["🥇", "🥈", "🥉"]
    colors = ['#FFD700','#C0C0C0','#CD7F32']  # Gold, Silver, Bronze

    for i, row in top3.iterrows():
        st.markdown(
            f"<div style='background-color:{colors[i]}; padding:10px; border-radius:10px'>"
            f"<h3>{medals[i]} {row['employee_name']} — {int(row['points'])} pts</h3>"
            f"<b>Level:</b> {row['level']} | <b>Badge:</b> {row['badge']}<br>"
            f"<i>{row['nudge']}</i></div>",
            unsafe_allow_html=True
        )
        st.progress(min(row['progress'], 1.0))

    # ----------------------------
    # 7. Full Leaderboard
    # ----------------------------
    st.subheader("📋 Full Leaderboard")
    df_leaderboard = df.sort_values('points', ascending=False).reset_index(drop=True)

    # Add rank column
    df_leaderboard.index += 1
    df_leaderboard['Rank'] = df_leaderboard.index

    # Select and rename columns for display
    table_df = df_leaderboard[['Rank', 'employee_name', 'points', 'level', 'badge', 'nudge', 'progress']]
    table_df.rename(columns={
        'employee_name': 'Employee',
        'points': 'Points',
        'level': 'Level',
        'badge': 'Badge',
        'nudge': 'Nudge',
        'progress': 'Progress'
    }, inplace=True)

    # Display as scrollable dataframe (with height 400px)
    st.dataframe(table_df, height=400)

    # ----------------------------
    # 8. Charts
    # ----------------------------
    st.subheader("📈 Points Distribution")
    st.bar_chart(df[['employee_name','points']].set_index('employee_name'))

    st.subheader("🎖️ Level Distribution")
    st.bar_chart(df['level'].value_counts())

    st.subheader("🏅 Badge Distribution")
    st.bar_chart(df['badge'].value_counts())

    st.subheader("🚀 Progress Toward Top Performer")
    st.bar_chart(df[['employee_name','progress']].set_index('employee_name'))

    # ----------------------------
    # 9. Export Analytics Report
    # ----------------------------
    st.subheader("💾 Export Analytics Report")
    csv = df[['employee_name','points','level','badge','nudge','progress']].to_csv(index=False)
    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name='analytics_report.csv',
        mime='text/csv'
    )

else:
    st.info("Please upload a KPI CSV or Excel file to view the dashboard.")