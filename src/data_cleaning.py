import pandas as pd
import numpy as np
import os
import re

def parse_salary(salary_str):
    if pd.isna(salary_str) or salary_str == '-1' or salary_str == -1:
        return pd.Series([np.nan, np.nan, np.nan])
    try:
        # Remove (Glassdoor est.) or similar trailing notes
        clean_str = str(salary_str).split('(')[0]
        # Remove Employer Provided Salary prefix if present
        if 'Employer Provided Salary:' in clean_str:
            clean_str = clean_str.replace('Employer Provided Salary:', '')
        
        # Check if hourly
        is_hourly = 'Per Hour' in clean_str
        if is_hourly:
            clean_str = clean_str.replace('Per Hour', '')
            
        clean_str = clean_str.replace('K', '').replace('$', '').strip()
        
        parts = clean_str.split('-')
        if len(parts) == 2:
            min_s = float(parts[0])
            max_s = float(parts[1])
            
            # If hourly, rough conversion to annual 'K'
            if is_hourly:
                min_s = (min_s * 2080) / 1000
                max_s = (max_s * 2080) / 1000
                
            return pd.Series([min_s, max_s, (min_s + max_s) / 2])
    except Exception as e:
        print(f"Warning: could not parse salary '{salary_str}': {e}")
    return pd.Series([np.nan, np.nan, np.nan])

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Drop index column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Replace known missing value indicators with NaNs
    print("Standardizing missing value representations...")
    df = df.replace(['-1', -1, '-1.0', -1.0, 'Unknown', 'Unknown / Non-Applicable'], np.nan)
    
    # Salary Parsing
    print("Parsing Salary Estimate...")
    df[['min_salary_k', 'max_salary_k', 'avg_salary_k']] = df['Salary Estimate'].apply(parse_salary)
    
    # Company Name Check
    print("Cleaning Company Name...")
    # Many company names end with a newline and rating (e.g. "Google\n4.5"), split and take first part
    df['Company Name'] = df['Company Name'].apply(lambda x: str(x).split('\n')[0] if pd.notna(x) else x)
    
    # Location Check
    print("Extracting Job State from Location...")
    # Standard format: 'City, State' -> extracting state
    df['Job State'] = df['Location'].apply(lambda x: str(x).split(',')[-1].strip() if pd.notna(x) and ',' in str(x) else str(x))
    
    # Reorder some key columns to the front for easier viewing
    cols = list(df.columns)
    important_cols = ['Job Title', 'Company Name', 'Location', 'Job State', 'min_salary_k', 'max_salary_k', 'avg_salary_k']
    # remove them from original order
    for c in important_cols:
        if c in cols: cols.remove(c)
    # prepend
    df = df[important_cols + cols]

    print(f"Saving cleaned dataset to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print("Data cleaning completed successfully!")
    print(f"Original shape: {pd.read_csv(input_path).shape}")
    print(f"Cleaned shape: {df.shape}")

if __name__ == "__main__":
    import os
    # Project root is expected to be the cwd
    raw_data_path = 'data/raw/DataAnalyst.csv'
    processed_data_path = 'data/processed/cleaned_jobs.csv'
    
    if os.path.exists(raw_data_path):
        clean_data(raw_data_path, processed_data_path)
    else:
        print(f"Error: {raw_data_path} not found. Ensure you are running from the project root.")
