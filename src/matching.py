from src.config import ACCOUNT_ALIASES
from src.preprocessing import aggregate_accounts
from rapidfuzz import process, fuzz

def alias_matching(df):
    df=df.copy()
    df['Account']=df['Account'].map(ACCOUNT_ALIASES).fillna(df['Account'])
    return df


def fuzzy_matching(source_df, reference_df, threshold=90):
    source_df = source_df.copy()
    reference_names = reference_df['Account'].unique()
    for acc in source_df['Account'].unique():
        match = process.extractOne(
            query=acc,
            choices=reference_names,
            scorer=fuzz.WRatio,
        )
        if match is not None and match[1] >= threshold:
            source_df.loc[source_df['Account'] == acc, "Account"] = match[0]
    return source_df

def match_accounts(gl_df, tb_df):
    gl_df = alias_matching(gl_df)
    tb_df = alias_matching(tb_df)
    matched_gl_df = fuzzy_matching(gl_df, tb_df, threshold=90)
    matched_tb_df = fuzzy_matching(tb_df, matched_gl_df, threshold=90)
    gl_aggregate = aggregate_accounts(matched_gl_df)
    tb_aggregate = aggregate_accounts(matched_tb_df)
    return gl_aggregate, tb_aggregate

