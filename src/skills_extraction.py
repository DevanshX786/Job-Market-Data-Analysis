import pandas as pd
import os
import re

def extract_skills(input_path, output_path):
    print(f"Loading cleaned dataset from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Define the fundamental tools/skills we want to search for
    # Using explicit regex patterns to avoid substring matches
    # e.g., we want ' R ' or R, but not 'Retail'
    skills_regex = {
        'Python': r'\bpython\b',
        'SQL': r'\bsql\b',
        'Excel': r'\bexcel\b',
        'Tableau': r'\btableau\b',
        'Power BI': r'\bpower\s*bi\b',
        'R': r'\br\b',   # Just the letter R as a word
        'AWS': r'\baws\b',
        'Spark': r'\bspark\b',
        'Machine Learning': r'\bmachine learning\b|\bml\b'
    }
    
    print("Extracting skills from job descriptions...")
    # Make sure Job Description has no NaNs
    job_desc = df['Job Description'].fillna('').astype(str).str.lower()
    
    for skill, pattern in skills_regex.items():
        # Will True/False if the pattern exists in the string
        col_name = f'Requires_{skill}'
        df[col_name] = job_desc.str.contains(pattern, flags=re.IGNORECASE, regex=True)
    
    print("Skills extracted successfully!")
    
    print(f"Saving enriched dataset to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    # Quick sanity check on how many jobs require each skill
    print("\nSkill Demand Summary:")
    for skill in skills_regex.keys():
        count = df[f'Requires_{skill}'].sum()
        pct = (count / len(df)) * 100
        print(f"{skill}: {count} jobs ({pct:.1f}%)")

if __name__ == "__main__":
    input_csv = 'data/processed/cleaned_jobs.csv'
    output_csv = 'data/processed/enriched_jobs.csv'
    
    if os.path.exists(input_csv):
        extract_skills(input_csv, output_csv)
    else:
        print(f"Error: Could not find {input_csv}. Please run the data cleaning step first.")
