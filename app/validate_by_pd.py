import re

import pandas as pd


def extract_salary_range(salary_str):
    cleaned_salary = re.sub(r'[^\d–]', '', salary_str)

    salary_parts = cleaned_salary.split('–')

    try:
        if len(salary_parts) == 1:
            min_salary = max_salary = int(salary_parts[0])
        elif len(salary_parts) == 2:
            min_salary = int(salary_parts[0])
            max_salary = int(salary_parts[1])
        else:
            min_salary = max_salary = None
    except ValueError:
        min_salary, max_salary = None, None

    return min_salary, max_salary


df = pd.read_csv("job_data.csv")

df_cleaned = df[df['salary'].notna() & (df['salary'] != "N/A")]

df_cleaned[['min_salary', 'max_salary']] = df_cleaned['salary'].apply(
    lambda x: pd.Series(extract_salary_range(x))
)


df_cleaned.to_csv("job_data_cleaned.csv", index=False, encoding='utf-8')

print(df_cleaned)
