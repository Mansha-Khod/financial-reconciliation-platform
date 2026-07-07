import pandas as pd
from src.config import COLUMN_ALIASES,REQUIRED_COLUMNS


def load_csv(file):
    try:
        df=pd.read_csv(file)
        return df
    except Exception as e:
        print(f"ERROR : {e}")
        return None

def standardize_columns(df):
    changes={}
    for col in df.columns:
        for standard_column,alaises in COLUMN_ALIASES.items():
            if col==standard_column:
                continue
            elif col in alaises:
                df.rename(
                    columns={col: standard_column},
                    inplace=True
                )
                changes[col]=standard_column
                break 
    return df,changes


def validate_schema(df):
    missing=[]
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)
    return missing

def validate_missing_values(df):
    missing_counts=df.isnull().sum()
    missing_val={}
    for column,count in missing_counts.items():
        if count>0:
            missing_val[column]=count
    return missing_val


def validate_duplicates(df):
    return df.duplicated().sum()



            

            

