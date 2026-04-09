import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# 4. Basic Visualizations

# Optional: reduce dataset size for faster plotting
df_sample = df.sample(n=min(5000, len(df)), random_state=42)

# --- 2. Boxplot (outliers) ---
if 'Flow Bytes/s' in df.columns:
    plt.figure()
    sns.boxplot(x=df['Flow Bytes/s'].replace([float('inf'), -float('inf')], pd.NA).dropna())
    plt.title('Boxplot of Flow Bytes/s')
    plt.show()

# --- 3. Correlation Heatmap ---
plt.figure(figsize=(12, 8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# --- 4. Class Distribution ---
if 'Label' in df.columns:
    plt.figure()
    df['Label'].value_counts().plot(kind='bar')
    plt.title('Class Distribution')
    plt.xlabel('Class')
    plt.ylabel('Count')
    plt.show()

# --- 5. Scatter Plot ---
if all(col in df.columns for col in ['Flow Duration', 'Flow Bytes/s', 'Label']):
    plt.figure()
    sns.scatterplot(
        data=df_sample,
        x='Flow Duration',
        y='Flow Bytes/s',
        hue='Label',
        legend=False
    )
    plt.title('Flow Duration vs Flow Bytes/s')
    plt.show()



# Επιλογή μερικών χαρακτηριστικών για οπτικοποίηση
features_to_plot = ['Flow Duration', 'Total Fwd Packets', 'Fwd Packet Length Max', 'Flow Packets/s']

# Δημιουργία υπογραφημάτων (subplots)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
fig.suptitle('Boxplots για τον Εντοπισμό Ακραίων Τιμών', fontsize=16)

# Μετατροπή των axes σε επίπεδη λίστα για εύκολη προσπέλαση
axes = axes.flatten()

for i, col in enumerate(features_to_plot):
    if col in df.columns:
        # Καθαρισμός από άπειρες τιμές (inf) για το γράφημα
        clean_data = df[col].replace([float('inf'), -float('inf')], pd.NA).dropna()
        
        sns.boxplot(x=clean_data, ax=axes[i], color='skyblue')
        axes[i].set_title(f'Distribution of {col}')
        axes[i].set_xlabel('')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()



features = ['Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Flow Bytes/s']
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.flatten()

for i, feature in enumerate(features):
    if feature in df.columns:
        # Μετατροπή σε αριθμητικά και διαχείριση σφαλμάτων (π.χ. "Infinity")
        data_clean = pd.to_numeric(df[feature], errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()
        
        # Τώρα το data_clean περιέχει μόνο έγκυρους αριθμούς
        axes[i].hist(data_clean, bins=50, color='teal', edgecolor='black', log=True)
        axes[i].set_title(f'Histogram of {feature} (Log Scale)')
        axes[i].set_xlabel(feature)
        axes[i].set_ylabel('Frequency (log)')

plt.tight_layout()
plt.show()



# Προετοιμασία των δεδομένων του δείγματος
df['Flow Duration'] = pd.to_numeric(df['Flow Duration'], errors='coerce')
df['Flow Bytes/s'] = pd.to_numeric(df['Flow Bytes/s'], errors='coerce')

# Αφαίρεση τυχόν NaN που προέκυψαν από το "Infinity"
plot_data = df_sample[['Flow Duration', 'Flow Bytes/s', 'Label']].dropna()

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=np.log1p(plot_data['Flow Duration']), 
    y=np.log1p(plot_data['Flow Bytes/s']), 
    hue=plot_data['Label'],
    alpha=0.6
)
plt.title('Log-Log Scatter Plot: Duration vs Bytes/s [EDA]')
plt.xlabel('log(Flow Duration + 1)')
plt.ylabel('log(Flow Bytes/s + 1)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') # Εμφάνιση υπομνήματος έξω από το γράφημα
plt.show()