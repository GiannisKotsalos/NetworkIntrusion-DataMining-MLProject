import pandas as pd

# 1. Load the dataset
# Replace 'cic_ids_2017.csv' with the actual name or path of your CSV file
print("Loading dataset...")
df = pd.read_csv('cic_ids_2017.csv')

# 2. Calculate the basic summary statistics
# This function calculates count, mean, std, min, 25%, 50%, 75%, and max
print("Calculating summary statistics...")
summary_stats = df.describe()

# 3. Print the results to the console
print("\n--- Basic Summary Statistics ---")
print(summary_stats)

# 4. (Optional) Save the statistics to a new CSV file for easier viewing
# Since the CIC-IDS dataset has nearly 80 columns, viewing it in the console can be messy.
# Saving it to a CSV allows you to open it neatly in Excel.
summary_stats.to_csv('dataset_summary_statistics.csv')
print("\nStatistics successfully saved to 'dataset_summary_statistics.csv'")