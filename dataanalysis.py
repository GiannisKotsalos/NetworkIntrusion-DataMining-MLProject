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

def clean_data(df):
    """
    Καθαρίζει το dataset (NaNs, άπειρες τιμές, διπλότυπα), εκτυπώνει 
    τα αποτελέσματα του καθαρισμού και επιστρέφει το καθαρό dataframe.
    """
    print("\n" + "="*50)
    print(" 2. ΚΑΘΑΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ")
    print("="*50)
    
    initial_shape = df.shape
    
    # 1. Διαχείριση Άπειρων και Ελλιπών Τιμών
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    total_missing = df.isnull().sum().sum()
    df.dropna(inplace=True)
    
    # 2. Διαχείριση Διπλότυπων Εγγραφών
    total_duplicates = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    
    final_shape = df.shape
    
    print("[+] Ο καθαρισμός ολοκληρώθηκε επιτυχώς!")
    print(f"    - Αρχικές διαστάσεις: {initial_shape}")
    print(f"    - Αφαιρέθηκαν {total_missing} ελλιπείς/άπειρες τιμές.")
    print(f"    - Αφαιρέθηκαν {total_duplicates} διπλότυπες εγγραφές.")
    print(f"    - Τελικές διαστάσεις: {final_shape}")
    
    return df

def show_visualizations(df):
    """
    Δημιουργεί και εμφανίζει τα γραφήματα (EDA).
    """
    print("\n" + "="*50)
    print(" 3. ΕΜΦΑΝΙΣΗ ΓΡΑΦΗΜΑΤΩΝ (EDA)")
    print("="*50)
    print("Φόρτωση γραφημάτων... (Κλείστε κάθε παράθυρο γραφήματος για να εμφανιστεί το επόμενο)\n")

    # Δημιουργία δείγματος για πιο γρήγορα scatter plots
    df_sample = df.sample(n=min(5000, len(df)), random_state=42)

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

    # --- 3. Correlation Heatmap ---
    plt.figure(figsize=(12, 8))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, cmap='coolwarm')
    plt.title('Correlation Heatmap')
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

def main():
    print("Γίνεται φόρτωση του Dataset. Παρακαλώ περιμένετε...")
    try:
        df = pd.read_csv('archive/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print("Σφάλμα: Το αρχείο δεν βρέθηκε. Ελέγξτε τη διαδρομή (path).")
        sys.exit(1)

    is_cleaned = False

    while True:
        print("\n" + "*"*40)
        print("          ΜΕΝΟΥ ΕΠΙΛΟΓΩΝ          ")
        print("*"*40)
        print("1. Παρουσίαση Δομής & Στατιστική Ανάλυση")
        print("2. Καθαρισμός Δεδομένων (Drop NaNs & Duplicates)")
        print("3. Εμφάνιση Γραφημάτων (Visualizations)")
        print("4. Έξοδος")
        print("*"*40)
        
        choice = input("Επιλέξτε μια ενέργεια (1-4): ")
        
        if choice == '1':
            analyze_data(df, is_cleaned)
            
        elif choice == '2':
            if not is_cleaned:
                df = clean_data(df)
                is_cleaned = True
            else:
                print("\n[!] Το dataset έχει ήδη καθαριστεί.")
                
        elif choice == '3':
            if not is_cleaned:
                print("\n[!] Προσοχή: Εμφανίζονται γραφήματα με μη καθαρισμένα δεδομένα.")
            show_visualizations(df)
            
        elif choice == '4':
            print("Έξοδος από το πρόγραμμα. Καλή συνέχεια!")
            break
            
        else:
            print("Μη έγκυρη επιλογή. Παρακαλώ επιλέξτε από το 1 έως το 4.")

if __name__ == "__main__":
    main()