
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Printing Press Scheduler", layout="wide")
st.title("🖨️ Printing Press Scheduler")

if "jobs" not in st.session_state:
    st.session_state.jobs = []

def board_width(raw_code):
    try:
        width_raw = raw_code[4:10]
        inches = int(width_raw[:2])
        frac = int(width_raw[2:])
        return inches + frac / 1000
    except:
        return 0

def determine_press(width):
    return "Heidelberg" if width > 50 else "Kidder"

def calculate_hours(rolls, rate):
    return rolls / rate

st.sidebar.header("Add a Job")
job_id = st.sidebar.text_input("Job ID")
board_code = st.sidebar.text_input("Raw Board Code (e.g. B206500708C)")
rolls = st.sidebar.number_input("Number of Rolls", step=1)
rate = st.sidebar.number_input("Rate per Hour", value=5.0)
run_by = st.sidebar.date_input("Run By Date")
start_time = st.sidebar.time_input("Preferred Start Time", value=datetime.now().time())

if st.sidebar.button("Add Job"):
    width = board_width(board_code)
    press = determine_press(width)
    hours = calculate_hours(rolls, rate)
    start_dt = datetime.combine(run_by, start_time)
    end_dt = start_dt + timedelta(hours=hours)
    st.session_state.jobs.append({
        "Job ID": job_id,
        "Board Code": board_code,
        "Width": width,
        "Press": press,
        "Rolls": rolls,
        "Rate": rate,
        "Start": start_dt,
        "End": end_dt
    })
    st.sidebar.success(f"Added job {job_id} to {press}")

st.subheader("Scheduled Jobs")
if st.session_state.jobs:
    df = pd.DataFrame(st.session_state.jobs)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Schedule as CSV", csv, "schedule.csv", "text/csv")
else:
    st.info("No jobs scheduled yet.")
