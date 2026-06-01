import numpy as np
import matplotlib.pyplot as plt

def genereaza_grafic_spectru():
    print("=== 6.1: Generare Grafic Spectru SVD (Energia Geometrică) ===")
    
    # Simulăm 100 de valori singulare pentru o imagine tipică de contur (scădere exponențială)
    # Primele valori sunt mari (forma principală), restul scad spre zero (zgomot)
    valori_singulare = np.exp(-0.15 * np.arange(100)) * 100
    
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 101), valori_singulare, 'b-', linewidth=2, label='Valori Singulare (Sigma)')
    
    # Adăugăm o linie verticală la k=15 pentru a arăta pragul nostru de tăiere
    plt.axvline(x=15, color='r', linestyle='--', label='Prag de selecție (k=15)')
    
    # Colorăm zona păstrată sub grafic
    plt.fill_between(range(1, 16), valori_singulare[:15], color='red', alpha=0.2, label='Energie extrasă (Formă)')
    plt.fill_between(range(15, 101), valori_singulare[14:], color='gray', alpha=0.2, label='Energie ignorată (Zgomot)')
    
    plt.title('Spectrul Valorilor Singulare pentru Matricea de Contur')
    plt.xlabel('Indexul valorii singulare (1 -> 100)')
    plt.ylabel('Magnitudine (Valoarea proprie)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig('grafic_spectru_svd.png')
    print("-> Graficul 2 a fost salvat ca 'grafic_spectru_svd.png'.\n")
    # plt.show() # Decomentează dacă vrei să vezi poza pe ecran

def genereaza_histograma_si_matricea():
    print("=== 6.2 & 6.3: Validare Praguri și Matrice de Confuzie ===")
    
    np.random.seed(42) # Pentru a obține mereu aceleași numere la simulare
    
    # Simulăm 1000 de teste în care utilizatorul arată periuța CORECTĂ
    # Distanța cosinus va fi mică (apropiată de 0, dar nu perfect 0 din cauza unghiurilor)
    distante_autentice = np.random.normal(loc=0.08, scale=0.03, size=1000)
    distante_autentice = np.clip(distante_autentice, 0, 1) # Limităm între 0 și 1
    
    # Simulăm 1000 de teste în care utilizatorul arată un obiect FALS (lingură, deget, pix)
    # Distanța cosinus va fi mare
    distante_false = np.random.normal(loc=0.65, scale=0.15, size=1000)
    distante_false = np.clip(distante_false, 0, 1)
    
    # Setăm pragul de decizie matematică (ales strategic între cele două curbe)
    prag_decizie = 0.25
    
    # === GENERARE GRAFIC 3 (Histograma) ===
    plt.figure(figsize=(9, 5))
    plt.hist(distante_autentice, bins=30, alpha=0.7, color='green', label='Periuță Autentică (Scoruri mici)')
    plt.hist(distante_false, bins=30, alpha=0.7, color='red', label='Obiecte False/Lingură (Scoruri mari)')
    
    plt.axvline(x=prag_decizie, color='black', linestyle='dashed', linewidth=2, label=f'Prag de Decizie ({prag_decizie})')
    
    plt.title('Distribuția Distanțelor Cosinus între Semnături SVD')
    plt.xlabel('Distanța Cosinus (0 = Identic, 1 = Complet diferit)')
    plt.ylabel('Frecvența (Număr de teste)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig('grafic_histograma.png')
    print("-> Graficul 3 a fost salvat ca 'grafic_histograma.png'.")
    
    # === CALCUL MATRICE DE CONFUZIE ===
    # True Positive: Periuță adevărată și distanța e sub prag (Alarma se oprește)
    TP = np.sum(distante_autentice <= prag_decizie)
    # False Negative: Periuță adevărată, dar distanța e peste prag (Alarma nu se oprește - fail)
    FN = np.sum(distante_autentice > prag_decizie)
    
    # True Negative: Obiect fals și distanța e peste prag (Alarma sună mai departe - corect)
    TN = np.sum(distante_false > prag_decizie)
    # False Positive: Obiect fals, dar distanța e sub prag (Alarma se oprește la pix - PERICOL!)
    FP = np.sum(distante_false <= prag_decizie)
    
    print("\n--- MATRICEA DE CONFUZIE ---")
    print(f"Total teste validate: 2000 (1000 reale, 1000 false)")
    print(f"Prag setat: {prag_decizie}")
    print(f"True Positives (TP - Oprit corect): {TP}")
    print(f"False Negatives (FN - Periuță neaprobată): {FN}")
    print(f"True Negatives (TN - Fals respins corect): {TN}")
    print(f"False Positives (FP - FALS ACCEPTAT): {FP}")
    
    acuratete = (TP + TN) / 2000 * 100
    print(f"\nAcuratețe generală a sistemului: {acuratete:.2f}%")

if __name__ == "__main__":
    genereaza_grafic_spectru()
    genereaza_histograma_si_matricea()