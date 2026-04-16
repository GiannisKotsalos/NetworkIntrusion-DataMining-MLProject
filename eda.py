import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

def analyze_data(df, is_cleaned=False):
    """
    Τυπώνει την αναφορά δομής και τα περιγραφικά στατιστικά του dataset.
    Προσαρμόζεται ανάλογα με το αν τα δεδομένα είναι καθαρισμένα ή όχι.
    """
    print("\n" + "="*50)
    print(" 1. ΠΑΡΟΥΣΙΑΣΗ ΔΟΜΗΣ & ΣΤΑΤΙΣΤΙΚΗ ΑΝΑΛΥΣΗ")
    print("="*50)
    
    print(f"[+] Τρέχουσες διαστάσεις (Γραμμές, Στήλες): {df.shape}")

    if is_cleaned:
        print("\n[i] Κατάσταση: Το dataset είναι ΚΑΘΑΡΙΣΜΕΝΟ.")
    else:
        print("\n[!] Κατάσταση: Το dataset ΔΕΝ έχει καθαριστεί ακόμα.")
        # Εντοπισμός προβλημάτων χωρίς να πειράξουμε το αρχικό df
        temp_df = df.copy()
        temp_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        missing = temp_df.isnull().sum().sum()
        dups = temp_df.duplicated().sum()
        print(f"    - Εντοπίστηκαν {missing} ελλιπείς/άπειρες τιμές.")
        print(f"    - Εντοπίστηκαν {dups} διπλότυπες εγγραφές.")
        del temp_df # Διαγραφή του προσωρινού dataframe για εξοικονόμηση μνήμης

    print("\n" + "-" * 40)
    print(" Πληροφορίες Στηλών και Τύπων Δεδομένων")
    print("-" * 40)
    df.info() 

    print("\n" + "-" * 40)
    print(" Βασικά Περιγραφικά Στατιστικά (describe)")
    print("-" * 40)
    print(df.describe())



def show_visualizations(df):
    """
    Δημιουργεί και εμφανίζει τα γραφήματα (EDA).
    """
    print("\n" + "="*50)
    print(" 3. ΕΜΦΑΝΙΣΗ ΓΡΑΦΗΜΑΤΩΝ (EDA)")
    print("="*50)
    print("Φόρτωση γραφημάτων... (Κλείστε κάθε παράθυρο γραφήματος για να εμφανιστεί το επόμενο)\n")

    # Δημιουργία δείγματος για πιο γρήγορα scatter plots
    #df_sample = df.sample(n=min(5000, len(df)), random_state=42)

    # --- 1. Correlation Heatmap ---
    plt.figure(figsize=(20, 16)) # Increased size to accommodate many features
    corr = df.corr(numeric_only=True)

    # 1. Create a mask to hide the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 2. Plot the heatmap with mask, grid (linewidths), and fixed color range
    sns.heatmap(corr, 
                mask=mask, 
                cmap='coolwarm', 
                vmin=0, vmax=1,       # Anchors colors from -1 to 1
                linewidths=0.5,        # Creates the grid lines
                linecolor='white', # Sets the grid line color
                cbar_kws={"shrink": .8}) # Shrinks the colorbar slightly for aesthetics
    
    plt.title('Correlation Heatmap (Lower Triangle)', fontsize=18)
    plt.xticks(fontsize=10, rotation=90)
    plt.yticks(fontsize=10, rotation=0)
    plt.tight_layout()
    plt.show()

    # --- 1. Boxplot ---
    features_to_plot = ['Flow Duration', 'Total Fwd Packets', 'Fwd Packet Length Max', 'Flow Packets/s']
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
    fig.suptitle('Boxplots για τον Εντοπισμό Ακραίων Τιμών', fontsize=16)
    axes = axes.flatten()

    for i, col in enumerate(features_to_plot):
        if col in df.columns:
            clean_data = df[col].replace([float('inf'), -float('inf')], pd.NA).dropna()
            sns.boxplot(x=clean_data, ax=axes[i], color='skyblue')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel('')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # --- 2. Histograms ---
    features_hist = ['Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Flow Bytes/s']
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, feature in enumerate(features_hist):
        if feature in df.columns:
            data_clean = pd.to_numeric(df[feature], errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()
            axes[i].hist(data_clean, bins=50, color='teal', edgecolor='black', log=True)
            axes[i].set_title(f'Histogram of {feature} (Log Scale)')
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel('Frequency (log)')

    plt.tight_layout()
    plt.show()

    # --- 4. Class Distribution ---
    if 'Label' in df.columns:
        plt.figure(figsize=(8, 6))
        df['Label'].value_counts().plot(kind='bar', color='coral', edgecolor='black')
        plt.title('Κατανομή Κλάσεων (Class Distribution - Label)')
        plt.xlabel('Class')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # --- 5. Log-Log Scatter Plot ---
    if all(col in df.columns for col in ['Flow Duration', 'Flow Bytes/s', 'Label']):
        df_sample_safe = df_sample.copy()
        df_sample_safe['Flow Duration'] = pd.to_numeric(df_sample_safe['Flow Duration'], errors='coerce')
        df_sample_safe['Flow Bytes/s'] = pd.to_numeric(df_sample_safe['Flow Bytes/s'], errors='coerce')
        plot_data = df_sample_safe[['Flow Duration', 'Flow Bytes/s', 'Label']].dropna()

        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x=np.log1p(plot_data['Flow Duration']), 
            y=np.log1p(plot_data['Flow Bytes/s']), 
            hue=plot_data['Label'],
            alpha=0.6
        )
        plt.title('Log-Log Scatter Plot: Duration vs Bytes/s')
        plt.xlabel('log(Flow Duration + 1)')
        plt.ylabel('log(Flow Bytes/s + 1)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()


def show_all_boxplots_squeezed(df):
    """
    Δημιουργεί ένα ενιαίο, μεγάλο γράφημα με οριζόντια boxplots για όλες 
    τις αριθμητικές μεταβλητές, χρησιμοποιώντας λογαριθμική κλίμακα (symlog)
    και προσαρμοσμένα όρια για αποφυγή κενού χώρου.
    """
    print("\n" + "="*50)
    print(" ΔΗΜΙΟΥΡΓΙΑ ΣΥΓΚΕΝΤΡΩΤΙΚΟΥ BOXPLOT (LOG SCALE)")
    print("="*50)
    
    # Επιλογή μόνο των αριθμητικών στηλών
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        print("Δεν βρέθηκαν αριθμητικές στήλες.")
        return

    # Υπολογισμός του απόλυτου ελάχιστου και μέγιστου σε όλο το dataset
    global_min = df[numeric_cols].min().min()
    global_max = df[numeric_cols].max().max()

    fig_height = max(10, len(numeric_cols) * 0.3) 
    plt.figure(figsize=(15, fig_height))
    
    ax = sns.boxplot(data=df[numeric_cols], orient='h', palette='viridis', fliersize=2)
    ax.set_xscale('symlog')
    
    # --- ΝΕΟΣ ΚΩΔΙΚΑΣ: Διόρθωση του κενού χώρου (Whitespace) ---
    # Βάζουμε -1 στο αριστερό όριο για να φαίνονται καθαρά τα μηδενικά 
    # και πολλαπλασιάζουμε το δεξί όριο x10 (ένα "βήμα" στη λογαριθμική κλίμακα) 
    # για να μην ακουμπάνε οι τελείες στην άκρη της οθόνης.
    left_limit = global_min if global_min < 0 else -1
    right_limit = global_max * 10
    
    ax.set_xlim(left=left_limit, right=right_limit)
    # -----------------------------------------------------------
    
    plt.title('Συγκεντρωτικό Boxplot όλων των Χαρακτηριστικών (Προσαρμοσμένο Symlog)', fontsize=18)
    plt.xlabel('Τιμές (Συμμετρική Λογαριθμική Κλίμακα)', fontsize=12)
    plt.ylabel('Χαρακτηριστικά (Στήλες)', fontsize=12)
    
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()