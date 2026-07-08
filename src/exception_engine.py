

def top_mismatches(rec_df, n=5):
    sorted_df = rec_df.sort_values(by="Difference", key=lambda s: s.abs(), ascending=False)
    return sorted_df.head(n)

def generate_exception_report(rec_df):
    exception_df = rec_df[~rec_df["Status"].isin(["Matched", "Matched (Within Tolerance)"])]
    return exception_df

def missing_in_gl(rec_df):
    missing_gl=rec_df[rec_df['Status'] == "Missing in GL"]
    return missing_gl

def missing_in_tb(rec_df):
    missing_tb=rec_df[rec_df['Status'] == "Missing in TB"]
    return missing_tb

def get_mismatch(rec_df):
    mismatched=rec_df[rec_df['Status'] == "Mismatch"]
    return mismatched

def within_tolerance(rec_df):
    match_tol=rec_df[rec_df['Status']=='Matched (Within Tolerance)']
    return match_tol

