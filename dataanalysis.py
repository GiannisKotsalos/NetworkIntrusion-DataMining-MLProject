import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset
print("Loading dataset...")
df = pd.read_csv('archive/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')

# --- THE FIX ---
# Strip hidden whitespace from column names
df.columns = df.columns.str.strip()
# ---------------

# 2. Calculate the basic summary statistics
print("Calculating summary statistics...")
summary_stats = df.describe()

# 3. Print the results to the console
print("\n--- Basic Summary Statistics ---")
print(summary_stats)

# 4. Save the statistics to a new CSV file
summary_stats.to_csv('dataset_summary_statistics.csv')
print("\nStatistics successfully saved to 'dataset_summary_statistics.csv'")

# Analyze a few important columns
columns_to_plot = [
    'Destination Port', 
    'Flow Duration', 
    'Total Length of Fwd Packets', 
    'Fwd Packet Length Mean'
]

print("Generating plots...")

for col in columns_to_plot:
    # Create a wide figure to hold two plots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1. Histogram (to see the distribution pattern)
    sns.histplot(df[col], bins=50, ax=axes[0], color='blue')
    axes[0].set_title(f'Histogram of {col}')
    
    # Crucial trick for Network Data: Use a logarithmic scale!
    axes[0].set_yscale('log') 
    
    # 2. Boxplot (to see the spread and outliers)
    sns.boxplot(x=df[col], ax=axes[1], color='orange')
    axes[1].set_title(f'Boxplot of {col}')
    
    # Adjust layout and save the file
    plt.tight_layout()
    
    # Clean the column name just in case it has weird characters
    safe_col_name = col.replace('/', '_').replace(' ', '_')
    filename = f'plot_{safe_col_name}.png'
    
    plt.savefig(filename)
    # Close the figure to free up your Mac's memory
    plt.close(fig) 
    
    print(f"Saved: {filename}")

print("All plots generated successfully!")