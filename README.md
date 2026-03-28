# Job Market Data Analysis 📊

This project is a complete end-to-end Python data pipeline designed to analyze job market data and extract actionable insights about skills demand, salary trends, and hiring patterns for Data Analysts.

## 🗂️ Dataset Source
The data used in this project is sourced from Kaggle:
👉 [Data Analyst Jobs Dataset (by andrewmvd)](https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs)

*Note: The raw CSV file (`DataAnalyst.csv`) contains over 2,200 detailed job postings scraped from Glassdoor.*

---

## 🚀 Project Pipeline Flow

The project is structured into three modular, sequential Python scripts located in the `src/` directory.

### 1. Data Cleaning (`src/data_cleaning.py`)
**Input:** `data/raw/DataAnalyst.csv`  
**Output:** `data/processed/cleaned_jobs.csv`
*   **Action:** Standardizes missing values (handling `-1` and `Unknown` placeholders).
*   **Action:** Parses complex text blocks strings in the `Salary Estimate` column into functional numeric columns (`min_salary_k`, `max_salary_k`, `avg_salary_k`).
*   **Action:** Cleans the `Company Name` trailing metadata and extracts the distinct US `Job State` from the location string.

### 2. Skills Extraction (`src/skills_extraction.py`)
**Input:** `data/processed/cleaned_jobs.csv`  
**Output:** `data/processed/enriched_jobs.csv`
*   **Action:** Uses Python's Regular Expressions (`regex`) to scan the massive `Job Description` texts for highly-demanded technical tools (e.g. Python, SQL, Tableau, R, AWS, Spark).
*   **Action:** Engineers new binary feature columns (`True/False`) indicating out if a specific job posting explicitly requires a given skill.

### 3. Exploratory Data Analysis & Visualization (`src/analysis_and_viz.py`)
**Input:** `data/processed/enriched_jobs.csv`  
**Output:** `docs/*.png` (Saved Visualization Charts)
*   **Action:** Aggregates and calculates descriptive statistics using `pandas.groupby()`.
*   **Action:** Generates custom `seaborn` / `matplotlib` charts directly into the `docs/` folder:
    *   **Skill Demand**: Which tools are most commonly requested.
    *   **Salary Premiums**: Does knowing specific skills (like Machine Learning or AWS) increase your median salary above the baseline?
    *   **Top Paying States**: Aggregated salaries across US geography.

---

## 📚 Study Guides
If you are learning Python for data analysis, this repository includes heavily-commented study guides in the `docs/` folder explaining the mechanical pandas and plotting code line-by-line:
1. `docs/data_cleaning_study_guide.txt`
2. `docs/skills_extraction_study_guide.txt`
3. `docs/analysis_and_viz_study_guide.txt`

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/YourRepoName.git
   cd "YourRepoName"
   ```

2. **Set up the virtual environment & install requirements:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Download Data:**
   * Download `DataAnalyst.csv` from the Kaggle link above.
   * Place it entirely untouched into the `data/raw/` directory.

4. **Execute the Pipeline:**
   ```bash
   python src/data_cleaning.py
   python src/skills_extraction.py
   python src/analysis_and_viz.py
   ```
   *Your final PNG charts will appear in the `/docs` folder!*
