import pandas as pd
import numpy as np


def top_mismatches(rec_df, n=5):
    rec_df = rec_df.sort_values(by="Difference", key=lambda s: s.abs(), ascending=False)
    return rec_df.head(n)

def generate_exception_report(rec_df):
    exception_df = rec_df[~rec_df["Status"].isin(["Matched", "Matched (Within Tolerance)"])]
    return exception_df
