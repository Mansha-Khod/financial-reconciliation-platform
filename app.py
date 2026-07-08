import streamlit as st
import pandas as pd

from src.validation import (
    standardize_columns,
    validate_schema,
    validate_missing_values,
    validate_duplicates,
)

from src.preprocessing import (
    clean_account_names,
    clean_amount_column,
    convert_amount_to_numeric,
)

from src.matching import match_accounts

from src.reconciliation import perform_reconciliation

from src.kpi import (
    calculate_kpis,
    largest_variance,
)

from src.exception_engine import (
    generate_exception_report,
    top_mismatches,
)

from src.visualization import (
    plot_status_distribution,
    plot_top_variances,
    plot_gl_tb_totals,
    plot_difference_distribution,
)


st.set_page_config(
    page_title="Financial Reconciliation Platform",
    layout="wide",
)


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("Financial Reconciliation")

    st.markdown("---")

    st.write(
        """
This project validates, cleans and reconciles
General Ledger and Trial Balance files.

Features

- Data Validation
- Data Cleaning
- Alias Matching
- Fuzzy Matching
- Account Aggregation
- Financial Reconciliation
- KPI Generation
- Exception Reporting
- Interactive Dashboard
"""
    )


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("Financial Reconciliation & Data Quality Analytics Platform")

st.write(
    """
Upload a General Ledger and Trial Balance CSV file
to perform automated reconciliation.
"""
)

st.markdown("---")


# ---------------------------------------------------
# Upload Files
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    tb_file = st.file_uploader(
        "Upload Trial Balance",
        type="csv",
    )

with col2:

    gl_file = st.file_uploader(
        "Upload General Ledger",
        type="csv",
    )


# ---------------------------------------------------
# Run Pipeline
# ---------------------------------------------------

if tb_file is not None and gl_file is not None:

    tb_df = pd.read_csv(tb_file)
    gl_df = pd.read_csv(gl_file)

    # ---------------------------------------
    # Standardize Columns
    # ---------------------------------------

    tb_df, tb_changes = standardize_columns(tb_df)
    gl_df, gl_changes = standardize_columns(gl_df)

    # ---------------------------------------
    # Validation
    # ---------------------------------------

    tb_missing_columns = validate_schema(tb_df)
    gl_missing_columns = validate_schema(gl_df)

    tb_missing_values = validate_missing_values(tb_df)
    gl_missing_values = validate_missing_values(gl_df)

    tb_duplicates = validate_duplicates(tb_df)
    gl_duplicates = validate_duplicates(gl_df)

    st.header("Validation Summary")

    left, right = st.columns(2)

    with left:

        with st.expander("Trial Balance", expanded=True):

            st.write(
                "Missing Columns:",
                tb_missing_columns if tb_missing_columns else "None",
            )

            st.write(
                "Missing Values:",
                tb_missing_values if tb_missing_values else "None",
            )

            st.write(
                "Duplicate Rows:",
                tb_duplicates,
            )

            if tb_changes:

                st.write("Columns Renamed")

                st.json(tb_changes)

    with right:

        with st.expander("General Ledger", expanded=True):

            st.write(
                "Missing Columns:",
                gl_missing_columns if gl_missing_columns else "None",
            )

            st.write(
                "Missing Values:",
                gl_missing_values if gl_missing_values else "None",
            )

            st.write(
                "Duplicate Rows:",
                gl_duplicates,
            )

            if gl_changes:

                st.write("Columns Renamed")

                st.json(gl_changes)

    if tb_missing_columns or gl_missing_columns:

        st.error("Validation failed because required columns are missing.")

        st.stop()

    # ---------------------------------------
    # Preprocessing
    # ---------------------------------------

    tb_df = clean_account_names(tb_df)
    tb_df = clean_amount_column(tb_df)
    tb_df = convert_amount_to_numeric(tb_df)

    gl_df = clean_account_names(gl_df)
    gl_df = clean_amount_column(gl_df)
    gl_df = convert_amount_to_numeric(gl_df)

    # ---------------------------------------
    # Matching
    # ---------------------------------------

    gl_df, tb_df = match_accounts(gl_df, tb_df)

    # ---------------------------------------
    # Reconciliation
    # ---------------------------------------

    rec_df, summary = perform_reconciliation(
        tb_df,
        gl_df,
    )

    # ---------------------------------------
    # KPIs
    # ---------------------------------------

    kpis = calculate_kpis(
        rec_df,
        summary,
    )

    variance = largest_variance(rec_df)

    st.markdown("---")

    st.header("Financial KPIs")

    row1 = st.columns(3)

    row1[0].metric(
        "Total GL",
        f"{kpis['Total GL']:,.2f}",
    )

    row1[1].metric(
        "Total TB",
        f"{kpis['Total TB']:,.2f}",
    )

    row1[2].metric(
        "Net Difference",
        f"{kpis['Net Difference']:,.2f}",
    )

    row2 = st.columns(3)

    row2[0].metric(
        "Total Accounts",
        kpis["Total Accounts"],
    )

    row2[1].metric(
        "Match Rate",
        kpis["Match Rate"],
    )

    matched = (
        summary.get("Matched", 0)
        + summary.get("Matched (Within Tolerance)", 0)
    )

    row2[2].metric(
        "Matched Accounts",
        matched,
    )

    st.info(
        f"Largest Variance Account: "
        f"{variance['Largest Variance Account']} "
        f"({variance['Largest Variance Amount']:.2f})"
    )

    st.markdown("---")
        # ---------------------------------------
    # Charts
    # ---------------------------------------

    st.header("Dashboard")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.plotly_chart(
            plot_status_distribution(rec_df),
            width="stretch",
        )

        st.plotly_chart(
            plot_top_variances(rec_df),
            width="stretch",
        )

    with chart_col2:

        st.plotly_chart(
            plot_gl_tb_totals(rec_df),
            width="stretch",
        )

        st.plotly_chart(
            plot_difference_distribution(rec_df),
            width="stretch",
        )

    st.markdown("---")

    # ---------------------------------------
    # Reports
    # ---------------------------------------

    st.header("Reconciliation Report")

    st.dataframe(
        rec_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    exception_df = generate_exception_report(rec_df)

    st.header("Exception Report")

    st.dataframe(
        exception_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    st.header("Top 5 Mismatches")

    top5 = top_mismatches(rec_df)

    st.dataframe(
        top5,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    # ---------------------------------------
    # Downloads
    # ---------------------------------------

    st.header("Download Reports")

    download_col1, download_col2 = st.columns(2)

    with download_col1:

        st.download_button(
            label="Download Reconciliation Report",
            data=rec_df.to_csv(index=False),
            file_name="reconciliation_report.csv",
            mime="text/csv",
        )

        st.download_button(
            label="Download KPI Summary",
            data=pd.DataFrame([kpis]).to_csv(index=False),
            file_name="kpi_summary.csv",
            mime="text/csv",
        )

    with download_col2:

        st.download_button(
            label="Download Exception Report",
            data=exception_df.to_csv(index=False),
            file_name="exception_report.csv",
            mime="text/csv",
        )

        st.download_button(
            label="Download Top Mismatches",
            data=top5.to_csv(index=False),
            file_name="top_mismatches.csv",
            mime="text/csv",
        )

    st.markdown("---")

    st.success("Reconciliation completed successfully.")

else:

    st.info(
        "Upload both the Trial Balance and General Ledger CSV files to begin."
    )