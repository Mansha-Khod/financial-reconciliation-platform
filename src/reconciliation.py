import numpy as np
import pandas as pd

def perform_reconciliation(tb_df,gl_df):
    rec_df=gl_df.merge(tb_df,on='Account',how="outer",suffixes=('_GL','_TB'))

    rec_df['Difference']=(rec_df['Amount_GL']).fillna(0)-(rec_df['Amount_TB']).fillna(0)
    is_invalid_tb = rec_df['Amount_TB'].isna() | (rec_df['Amount_TB'] == 0)
    raw_variance = np.where(is_invalid_tb, np.nan, rec_df['Difference'] / rec_df['Amount_TB'])
    rec_df['Variance'] = [
        f"{x*100:.2f}%" if pd.notna(x) else "N/A" for x in raw_variance
    ]

    tolerance=1.00
    conditions=[
        rec_df['Amount_GL'].isna(),
        rec_df['Amount_TB'].isna(),
        rec_df['Difference']==0,
        rec_df['Difference'].abs()<=tolerance
    ]

    choices=[
        "Missing in GL",
        "Missing in TB",
        "Matched",
        "Matched (Within Tolerance)"
    ]

    rec_df['Status']=np.select(conditions,choices,default="Mismatch")
    summary=rec_df['Status'].value_counts().to_dict()
    return rec_df,summary