import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
from preprocessing import clean_data, remove_highly_correlated_features
from eda import analyze_data, show_visualizations, show_all_boxplots_squeezed



def main():
    print("Γίνεται φόρτωση του Dataset. Παρακαλώ περιμένετε...")
    try:
        df = pd.read_csv('archive/Wednesday-WorkingHours.pcap_ISCX.csv')
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
                df = remove_highly_correlated_features(df, threshold=0.90)
                is_cleaned = True
            else:
                print("\n[!] Το dataset έχει ήδη καθαριστεί και μειωθεί.")
                
        elif choice == '3':
            if not is_cleaned:
                print("\n[!] Προσοχή: Εμφανίζονται γραφήματα με μη καθαρισμένα δεδομένα.")
            show_visualizations(df)
            show_all_boxplots_squeezed(df)
            
        elif choice == '4':
            print("Έξοδος από το πρόγραμμα. Καλή συνέχεια!")
            break
            
        else:
            print("Μη έγκυρη επιλογή. Παρακαλώ επιλέξτε από το 1 έως το 4.")

if __name__ == "__main__":
    main()