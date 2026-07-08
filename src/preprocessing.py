import pandas as pd

def clean_account_names(df):
    if 'Account' in df.columns:
        df['Account'] = (
            df['Account']
            .astype(str)
            .str.strip()
            .str.replace(r'\s+', ' ', regex=True)
            .str.title()
        )
    return df

def clean_amount_column(df):
    if 'Amount' in df.columns:
        df['Amount']=(
            df['Amount']
            .astype(str)
            .str.replace(r'[^\d(),.-]','',regex=True))
    return df

def convert_amount_to_numeric(df):
    if 'Amount' in df.columns:
        df['Amount']=(
            df['Amount']
            .astype(str)
            .str.replace(",",'')
            .str.replace(r"\((\d+)\)",r'-\1',regex=True)
        ).pipe(pd.to_numeric,errors='coerce')
    return df 
def aggregate_accounts(df):
    df=df.copy()
    aggregated_df = (
    df.groupby("Account")["Amount"]
      .sum()
      .reset_index()
)
    return aggregated_df