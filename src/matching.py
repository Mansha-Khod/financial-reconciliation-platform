from src.config import ACCOUNT_ALIASES

def alias_matching(df):
    df=df.copy()
    df['Account']=df['Account'].map(ACCOUNT_ALIASES).fillna(df['Account'])
    return df