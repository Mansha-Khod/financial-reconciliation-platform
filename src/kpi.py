import numpy as np
import pandas as pd



def calculate_kpis(rec_df, summary):
    total = rec_df.shape[0]
    matched = rec_df['Status'].isin(['Matched', 'Matched (Within Tolerance)']).sum()
    missing = rec_df['Status'].isin(['Missing in GL', 'Missing in TB']).sum()

    match_rate = (matched / total) * 100
    completeness_rate = ((total - missing) / total) * 100
    data_quality_score = round((match_rate * 0.6) + (completeness_rate * 0.4), 2)

    val_dict = {
        "Total Accounts": total,
        "Match Rate": f"{match_rate:.2f}%",
        "Total GL": round(float(rec_df["Amount_GL"].sum()), 2),
        "Total TB": round(float(rec_df["Amount_TB"].sum()), 2),
        "Net Difference": round(float(rec_df["Amount_GL"].sum() - rec_df["Amount_TB"].sum()), 2),
        "Data Quality Score": f"{data_quality_score}/100",
    }
    kpi_summary = val_dict | summary
    return kpi_summary


def largest_variance(rec_df):
    max_ix = rec_df["Difference"].abs().idxmax()
    lar_var_kpi = {
        "Largest Variance Account": rec_df.loc[max_ix, "Account"],
        "Largest Variance Amount": rec_df.loc[max_ix, "Difference"],
    }
    return lar_var_kpi
