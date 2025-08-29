import streamlit as st
import subprocess
import os
import json

REPORT_JSON = "reports/result.json"
TESTS_PATH = "tests"

# ----------------------------
# Function to run pytest with live output
# ----------------------------
def run_tests_live(test_name=None):
    """
    Run pytest with live output. If test_name is None, run all tests.
    """
    if test_name:
        cmd = f"pytest {os.path.join(TESTS_PATH, test_name)} --json-report --json-report-file={REPORT_JSON}"
    else:
        cmd = f"pytest {TESTS_PATH} --json-report --json-report-file={REPORT_JSON}"

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    output_placeholder = st.empty()
    live_output = ""

    for line in process.stdout:
        live_output += line
        output_placeholder.code(live_output)

    process.wait()
    return process.returncode

# ----------------------------
# Get list of available test files
# ----------------------------
def get_test_files():
    """
    Return a list of test files in the tests/ folder.
    """
    return [f for f in os.listdir(TESTS_PATH) if f.startswith("test_") and f.endswith(".py")]

# ----------------------------
# Initialize session state for dashboard
# ----------------------------
if "summary_results" not in st.session_state:
    st.session_state.summary_results = None

# ----------------------------
# Main page layout
# ----------------------------
st.set_page_config(page_title="Test Dashboard", layout="wide")
st.title("📊 Selenium Test Dashboard")

# ----------------------------
# Button: Run all tests
# ----------------------------
if st.button("▶️ Run All Tests"):
    with st.spinner("Running all tests..."):
        run_tests_live()
        # Load summary after tests complete
        if os.path.exists(REPORT_JSON):
            with open(REPORT_JSON, "r", encoding="utf-8") as f:
                st.session_state.summary_results = json.load(f)

# ----------------------------
# Dropdown to run individual test
# ----------------------------
st.subheader("Run Individual Test")
test_files = get_test_files()
selected_test = st.selectbox("Select a test", test_files)

if st.button("▶️ Run Selected Test"):
    with st.spinner(f"Running {selected_test}..."):
        run_tests_live(selected_test)
        # Load summary after test completes
        if os.path.exists(REPORT_JSON):
            with open(REPORT_JSON, "r", encoding="utf-8") as f:
                st.session_state.summary_results = json.load(f)

# ----------------------------
# Reset Dashboard button (below individual test section)
# ----------------------------
if st.button("🔄 Reset Dashboard"):
    st.session_state.summary_results = None  # Clear summary only

# ----------------------------
# Show test summary
# ----------------------------
st.subheader("📋 Test Summary")

if st.session_state.summary_results:
    report_data = st.session_state.summary_results

    if "tests" in report_data:
        table_data = [
            {
                "Status": t.get("outcome"),
                "Test": t.get("nodeid"),
            }
            for t in report_data["tests"]
        ]

        # Render colored table with black text
        for row in table_data:
            color = "#d4edda" if row["Status"] == "passed" else "#f8d7da"
            st.markdown(
                f"<div style='background-color: {color}; padding: 5px; border-radius: 5px; color: black;'>"
                f"<b>Status:</b> {row['Status']} &nbsp;&nbsp; <b>Test:</b> {row['Test']}"
                f"</div>",
                unsafe_allow_html=True
            )
else:
    st.info("⚠️ No summary available. Run a test to generate it.")
