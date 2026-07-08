import plotly.express as px
from src.exception_engine import top_mismatches

def plot_status_distribution(rec_df):
    status_counts = (
    rec_df["Status"]
    .value_counts()
    .reset_index()
    )
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(
        status_counts,
        values="Count",
        names="Status",
        color="Status",
        hole=0.4,
        title="Reconciliation Status Distribution"
    )
    fig.update_traces(
    hovertemplate="Status: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>")
    return fig


def plot_top_variances(rec_df):
    top_mismatch=top_mismatches(rec_df)
    fig = px.bar(
        top_mismatch,
        x="Difference",
        y="Account",
        color="Account",
        orientation="h",
        labels={
            "Difference": "Difference",
            "Account": "Account"
        },
        title="Top 5 Account Variances"
    )
    fig.update_layout(
        bargap=0.3,
        showlegend=False
    )
    return fig

def plot_gl_tb_totals(rec_df):
    tb_total=rec_df['Amount_TB'].sum()
    gl_total=rec_df['Amount_GL'].sum()
    fig = px.bar(
    x=["TB", "GL"],
    y=[tb_total, gl_total],
    color=["TB", "GL"],
    title="General Ledger vs Trial Balance Totals"
    )
    fig.update_layout(
    bargap=0.5,            
    showlegend=False        
    )

    return fig

def plot_difference_distribution(rec_df):
    diff=rec_df['Difference']
    fig=px.histogram(
        x=diff,
        color_discrete_sequence=["#636EFA"],
        text_auto=True,
        nbins=30,
        title="Distribution of Reconciliation Differences"
    )
    return fig

    