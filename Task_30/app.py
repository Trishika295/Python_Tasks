
import streamlit as st
import pandas as pd
from pathlib import Path

from log_analyzer import read_log_file, analyze_logs, generate_report

st.set_page_config(
    page_title="Server Log Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        color: #26334D;
    }

    .subtitle {
        color: #68758B;
        font-size: 16px;
        margin-bottom: 24px;
    }

    div[data-testid="stMetric"] {
        background: #F5F7FA;
        border: 1px solid #E1E6EF;
        padding: 18px;
        border-radius: 12px;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("Server Log Analyzer")
st.markdown(
    '<div class="subtitle">'
    'Analyze HTTP server logs, track errors, identify frequent IPs, '
    'and discover the most requested endpoints.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload a server log file",
    type=["log", "txt", "csv"],
    help="Upload a log containing standard HTTP access log entries."
)

use_sample = st.checkbox("Use the included sample log", value=True)

if uploaded_file is not None:
    raw_text = uploaded_file.getvalue().decode("utf-8", errors="replace")
    source_name = uploaded_file.name
elif use_sample:
    sample_path = Path(__file__).parent / "data" / "sample.log"

    if sample_path.exists():
        raw_text = sample_path.read_text(
            encoding="utf-8", errors="replace"
        )
        source_name = "sample.log"
    else:
        raw_text = ""
        source_name = "No file"
        st.warning("The sample log was not found. Create data/sample.log.")
else:
    raw_text = ""
    source_name = "No file"

if raw_text.strip():
    import io

    records = []
    malformed = 0

    # Use StringIO so uploaded files and sample files follow
    # the same parsing process.
    for line in io.StringIO(raw_text):
        if not line.strip():
            continue

        from log_analyzer import parse_log_line
        record = parse_log_line(line)

        if record is None:
            malformed += 1
        else:
            records.append(record)

    stats = analyze_logs(records)

    st.caption(f"Source: {source_name}")

    st.subheader("Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Requests", f"{stats['total_requests']:,}")
    c2.metric("Unique IPs", f"{stats['unique_ips']:,}")
    c3.metric("Error Responses", f"{stats['error_count']:,}")
    c4.metric("Error Rate", f"{stats['error_rate']:.2f}%")

    c5, c6, c7 = st.columns(3)

    c5.metric("Successful (2xx)", stats["success_count"])
    c6.metric("Client Errors (4xx)", stats["client_error_count"])
    c7.metric("Server Errors (5xx)", stats["server_error_count"])

    if malformed:
        st.warning(f"{malformed} malformed or unsupported log lines were skipped.")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("HTTP Status Codes")

        status_df = pd.DataFrame(
            [
                {"Status Code": str(code), "Requests": count}
                for code, count in sorted(stats["status_counts"].items())
            ]
        )

        if not status_df.empty:
            st.bar_chart(
                status_df.set_index("Status Code"),
                y="Requests"
            )
        else:
            st.info("No valid status codes found.")

    with right:
        st.subheader("HTTP Methods")

        methods_df = pd.DataFrame(
            [
                {"Method": method, "Requests": count}
                for method, count in stats["methods"].most_common()
            ]
        )

        if not methods_df.empty:
            st.bar_chart(methods_df.set_index("Method"))
        else:
            st.info("No HTTP methods found.")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Top IP Addresses")

        ip_df = pd.DataFrame(
            stats["top_ips"],
            columns=["IP Address", "Request Count"]
        )

        if not ip_df.empty:
            st.dataframe(ip_df, use_container_width=True, hide_index=True)
            st.bar_chart(ip_df.set_index("IP Address"))
        else:
            st.info("No IP address data available.")

    with right:
        st.subheader("Most Requested Endpoints")

        endpoint_df = pd.DataFrame(
            stats["top_endpoints"],
            columns=["Endpoint", "Request Count"]
        )

        if not endpoint_df.empty:
            st.dataframe(
                endpoint_df,
                use_container_width=True,
                hide_index=True
            )
            st.bar_chart(endpoint_df.set_index("Endpoint"))
        else:
            st.info("No endpoint data available.")

    st.divider()

    st.subheader("HTTP Status Summary")

    all_status_df = pd.DataFrame(
        [
            {"Status Code": code, "Request Count": count}
            for code, count in sorted(stats["status_counts"].items())
        ]
    )

    st.dataframe(
        all_status_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Parsed Log Records")

    records_df = pd.DataFrame(records)

    if not records_df.empty:
        st.dataframe(
            records_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Parsed Records (CSV)",
            data=records_df.to_csv(index=False).encode("utf-8"),
            file_name="parsed_logs.csv",
            mime="text/csv"
        )

    report = generate_report(stats, malformed)

    st.download_button(
        "Download Summary Report (TXT)",
        data=report,
        file_name="summary_report.txt",
        mime="text/plain"
    )

    st.download_button(
        "Download Complete Report (CSV)",
        data=all_status_df.to_csv(index=False).encode("utf-8"),
        file_name="status_summary.csv",
        mime="text/csv"
    )

    with st.expander("View Text Summary Report"):
        st.code(report, language="text")

else:
    st.info("Upload a log file or enable the sample log to begin analysis.")

st.divider()

st.caption(
    "Python Log File Analyzer | File handling • Counter • "
    "String processing • Data analysis"
)
