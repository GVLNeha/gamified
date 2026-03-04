import pandas as pd

def load_kpi_data(file):
    """
    Load KPI data from CSV or Excel.
    Cleans column names (strip & lowercase).
    """
    if hasattr(file, "read"):  # Streamlit UploadedFile
        filename = file.name.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            raise ValueError("Uploaded file must be CSV or Excel")
    else:  # file path
        file = str(file)
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            raise ValueError("File must be CSV or Excel")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Ensure required columns exist
    required_columns = {'employee_name', 'deliveries_completed', 'sales_made', 'customer_rating', 'attendance_days'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

    return df

def clean_data(df):
    """
    Basic cleaning for your KPI data:
    - Convert KPI columns to numeric
    - Fill NaN values with 0
    """
    kpi_columns = ['deliveries_completed', 'sales_made', 'customer_rating', 'attendance_days']
    for col in kpi_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def format_leaderboard(df, top_n=10):
    """
    Returns top N performers sorted by points.
    """
    leaderboard = df.sort_values('points', ascending=False).head(top_n)
    return leaderboard[['employee_name', 'points', 'level', 'badge']]