import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
import os

def generate_visualizations(input_path, output_dir):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Set seaborn style for prettier charts
    plt_sns.set_theme(style="whitegrid")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Top Demanded Skills
    print("Generating Skill Demand Chart...")
    skills = ['Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'R', 'AWS', 'Spark', 'Machine Learning']
    skill_counts = {skill: df[f'Requires_{skill}'].sum() for skill in skills}
    skill_pct = {skill: (count / len(df)) * 100 for skill, count in skill_counts.items()}
    
    # Sort by percentage descending
    skill_pct_sorted = dict(sorted(skill_pct.items(), key=lambda item: item[1], reverse=True))
    
    plt.figure(figsize=(10, 6))
    ax = plt_sns.barplot(x=list(skill_pct_sorted.values()), y=list(skill_pct_sorted.keys()), palette="viridis")
    plt.title('Most Demanded Skills for Data Analysts', fontsize=16)
    plt.xlabel('Percentage of Job Postings (%)', fontsize=12)
    plt.ylabel('Skill', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'skill_demand.png'))
    plt.close()
    
    # 2. Top Paying States for Data Analysts
    print("Generating Top Paying States Chart...")
    # Group by Job State and calculate median average salary
    state_salary = df.groupby('Job State')['avg_salary_k'].median().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(10, 6))
    plt_sns.barplot(x=state_salary.values, y=state_salary.index, palette="mako")
    plt.title('Top 15 Highest Paying States for Data Analysts', fontsize=16)
    plt.xlabel('Median Salary ($K)', fontsize=12)
    plt.ylabel('State', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_paying_states.png'))
    plt.close()

    # 3. Salary Premium by Skill (Does knowing Python pay more?)
    print("Generating Salary Premium by Skill Chart...")
    skill_salaries = {}
    baseline_salary = df['avg_salary_k'].median()
    
    for skill in skills:
        col = f'Requires_{skill}'
        # Median salary of jobs that REQUIRE the skill
        median_sal = df[df[col] == True]['avg_salary_k'].median()
        if pd.notna(median_sal):
            skill_salaries[skill] = median_sal
            
    # Sort
    skill_sal_sorted = dict(sorted(skill_salaries.items(), key=lambda item: item[1], reverse=True))
    
    plt.figure(figsize=(10, 6))
    ax = plt_sns.barplot(x=list(skill_sal_sorted.keys()), y=list(skill_sal_sorted.values()), palette="rocket")
    
    # Add a horizontal line for the baseline (overall median salary)
    plt.axhline(baseline_salary, color='red', linestyle='--', label=f'Overall Median (${baseline_salary}K)')
    
    plt.title('Median Salary by Required Skill', fontsize=16)
    plt.xlabel('Required Skill', fontsize=12)
    plt.ylabel('Median Salary ($K)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'salary_by_skill.png'))
    plt.close()

    print(f"All visualizations saved successfully in {output_dir}/ !")

if __name__ == "__main__":
    input_csv = 'data/processed/enriched_jobs.csv'
    output_dir = 'docs'
    if os.path.exists(input_csv):
        generate_visualizations(input_csv, output_dir)
    else:
        print(f"Error: Could not find {input_csv}. Please run the skills extraction step first.")
