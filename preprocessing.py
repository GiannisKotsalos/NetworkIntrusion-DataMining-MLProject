import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

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

    # 3. Αφαίρεση παράλογων αρνητικών τιμών (Data Sanity Check)
    # Ξέρουμε ότι τα Bytes/s και Packets/s δεν μπορούν να είναι αρνητικά.
    columns_to_check = ['Flow Bytes/s', 'Flow Packets/s']
    
    for col in columns_to_check:
        if col in df.columns:
            # Βρίσκουμε πόσες αρνητικές τιμές υπάρχουν για την αναφορά
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                print(f"    - Εντοπίστηκαν {negative_count} παράλογες αρνητικές τιμές στη στήλη '{col}'. Διαγράφονται.")
                # Κρατάμε μόνο τις γραμμές όπου η τιμή είναι >= 0
                df = df[df[col] >= 0]
    
    final_shape = df.shape
    
    print("[+] Ο καθαρισμός ολοκληρώθηκε επιτυχώς!")
    print(f"    - Αρχικές διαστάσεις: {initial_shape}")
    print(f"    - Αφαιρέθηκαν {total_missing} ελλιπείς/άπειρες τιμές.")
    print(f"    - Αφαιρέθηκαν {total_duplicates} διπλότυπες εγγραφές.")
    print(f"    - Τελικές διαστάσεις: {final_shape}")
    
    return df


def remove_highly_correlated_features(df, threshold=0.90):
    """
    Εντοπίζει και αφαιρεί στήλες που έχουν υψηλή συσχέτιση μεταξύ τους.
    Εκτυπώνει ποιες στήλες αφαιρέθηκαν για χρήση στην αναφορά.
    """
    print("\n" + "="*50)
    print(f" 3. ΕΠΙΛΟΓΗ ΧΑΡΑΚΤΗΡΙΣΤΙΚΩΝ (Threshold: {threshold})")
    print("="*50)
    
    # 1. Υπολογισμός του πίνακα συσχέτισης σε απόλυτες τιμές
    corr_matrix = df.corr(numeric_only=True).abs()
    
    # 2. Επιλογή του άνω τριγώνου του πίνακα για αποφυγή διπλοεγγραφών
    upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # 3. Εύρεση στηλών με συσχέτιση μεγαλύτερη από το όριο
    to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > threshold)]
    
    # 4. Αφαίρεση των στηλών
    df_reduced = df.drop(columns=to_drop)
    
    # 5. Εκτύπωση αποτελεσμάτων για την αναφορά (PDF)
    print(f"[+] Βρέθηκαν {len(to_drop)} στήλες με συσχέτιση > {threshold}.")
    if len(to_drop) > 0:
        print("    Στήλες που αφαιρέθηκαν λόγω υψηλής συσχέτισης:")
        for col in to_drop:
            print(f"    - {col}")
            
    print(f"\n[i] Νέες διαστάσεις dataset: {df_reduced.shape}")
    
    return df_reduced