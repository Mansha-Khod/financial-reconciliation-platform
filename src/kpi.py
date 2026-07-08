import numpy as np
import pandas as pd


def calculate_kpis(rec_df, summary):
    val_dict = {
        "Total Accounts": rec_df.shape[0],
        "Match Rate": f"{((rec_df['Status'].isin(['Matched', 'Matched (Within Tolerance)']).sum())/rec_df.shape[0])*100:.2f}%",
        "Total GL": round(float((rec_df["Amount_GL"]).sum()), 2),
        "Total TB": round(float((rec_df["Amount_TB"]).sum()), 2),
        "Net Difference": round(float(((rec_df["Amount_GL"]).sum()) - ((rec_df["Amount_TB"]).sum())), 2),
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
