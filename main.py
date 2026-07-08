from src.validation import (
    load_csv,
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

import os
import pandas as pd


def print_validation_report(
    file_name,
    missing_columns,
    missing_values,
    duplicate_count,
    changes,
):
    print("\n" + "=" * 50)
    print(f"{file_name:^50}")
    print("=" * 50)

    print(f"Missing Columns : {missing_columns if missing_columns else 'None'}")
    print(f"Missing Values  : {missing_values if missing_values else 'None'}")
    print(f"Duplicate Rows  : {duplicate_count}")

    if changes:
        print("Columns Renamed :")
        for old, new in changes.items():
            print(f"  {old} --> {new}")
    else:
        print("Columns Renamed : None")


def main():

    tb_path = input("Enter Trial Balance file path: ").strip()
    gl_path = input("Enter General Ledger file path: ").strip()

    tb_df = load_csv(tb_path)
    gl_df = load_csv(gl_path)

    if tb_df is None or gl_df is None:
        print("Unable to load one or more files.")
        return

    # -----------------------------
    # Standardize Columns
    # -----------------------------

    tb_df, tb_changes = standardize_columns(tb_df)
    gl_df, gl_changes = standardize_columns(gl_df)

    # -----------------------------
    # Validation
    # -----------------------------

    tb_missing_columns = validate_schema(tb_df)
    gl_missing_columns = validate_schema(gl_df)

    tb_missing_values = validate_missing_values(tb_df)
    gl_missing_values = validate_missing_values(gl_df)

    tb_duplicates = validate_duplicates(tb_df)
    gl_duplicates = validate_duplicates(gl_df)

    print_validation_report(
        "TRIAL BALANCE",
        tb_missing_columns,
        tb_missing_values,
        tb_duplicates,
        tb_changes,
    )

    print_validation_report(
        "GENERAL LEDGER",
        gl_missing_columns,
        gl_missing_values,
        gl_duplicates,
        gl_changes,
    )

    if tb_missing_columns or gl_missing_columns:
        print("\nValidation failed. Required columns are missing.")
        return

    # -----------------------------
    # Preprocessing
    # -----------------------------

    tb_df = clean_account_names(tb_df)
    tb_df = clean_amount_column(tb_df)
    tb_df = convert_amount_to_numeric(tb_df)

    gl_df = clean_account_names(gl_df)
    gl_df = clean_amount_column(gl_df)
    gl_df = convert_amount_to_numeric(gl_df)

    # -----------------------------
    # Matching
    # -----------------------------

    gl_df, tb_df = match_accounts(gl_df, tb_df)

    # -----------------------------
    # Reconciliation
    # -----------------------------

    rec_df, summary = perform_reconciliation(tb_df, gl_df)

    # -----------------------------
    # KPIs
    # -----------------------------

    kpis = calculate_kpis(rec_df, summary)
    variance = largest_variance(rec_df)

    print("\nKPI SUMMARY")
    print("-" * 40)

    for key, value in kpis.items():
        print(f"{key}: {value}")

    print("\nLargest Variance")
    print(variance)

    # -----------------------------
    # Exceptions
    # -----------------------------

    exception_df = generate_exception_report(rec_df)
    top5 = top_mismatches(rec_df)

    # -----------------------------
    # Save Reports
    # -----------------------------

    os.makedirs("outputs/reports", exist_ok=True)

    rec_df.to_csv(
        "outputs/reports/reconciliation_report.csv",
        index=False,
    )

    exception_df.to_csv(
        "outputs/reports/exception_report.csv",
        index=False,
    )

    top5.to_csv(
        "outputs/reports/top_mismatches.csv",
        index=False,
    )

    pd.DataFrame([kpis]).to_csv(
        "outputs/reports/kpi_summary.csv",
        index=False,
    )

    # -----------------------------
    # Save Charts
    # -----------------------------

    os.makedirs("outputs/charts", exist_ok=True)

    plot_status_distribution(rec_df).write_html(
        "outputs/charts/status_distribution.html"
    )

    plot_top_variances(rec_df).write_html(
        "outputs/charts/top_variances.html"
    )

    plot_gl_tb_totals(rec_df).write_html(
        "outputs/charts/gl_vs_tb.html"
    )

    plot_difference_distribution(rec_df).write_html(
        "outputs/charts/difference_distribution.html"
    )

    print("\nReconciliation completed successfully.")
    print("Reports saved to outputs/reports/")
    print("Charts saved to outputs/charts/")


if __name__ == "__main__":
    main()