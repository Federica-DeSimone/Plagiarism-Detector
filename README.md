# Plagiarism Detector
# 1. Introduzione generale al progetto
Il progetto che presento consiste nella realizzazione di un sistema informatico per l’analisi di
similarità e il rilevamento del **plagio musicale**. L’obiettivo non è stabilire se due brani siano identici
dal punto di vista dell’ascolto, ma verificare se condividono una struttura musicale profonda, anche
quando una melodia è stata modificata tramite trasposizione, variazioni ritmiche o cambi di tonalità.
Il progetto nasce dall’unione di tre ambiti fondamentali: 
 - 🎼 musica, come fenomeno sonoro strutturato
 - 📐 matematica, come linguaggio per descrivere relazioni e trasformazioni
 - 💻 informatica, comestrumento per automatizzare l’analisi
 
L’altezza di una nota è direttamente legata alla sua frequenza. Tuttavia, lavorare direttamente con le
frequenze reali sarebbe scomodo dal punto di vista computazionale.
Per questo motivo il progetto utilizza il **sistema MIDI**, che assegna a ogni nota un numero intero

# 2. Parte musicale del progetto: le rappresentazioni
## 2.1 Estrazione delle note
Attraverso la libreria **music21**, il programma legge file MIDI o MusicXML e ricava una lista ordinata di
note.
Ogni nota è descritta da: 
-  pitch (altezza MIDI)
-  duration (durata)
-  note_name (nome simbolico)

# 3. Parte matematica: confronto e similarità
## 3.1 Trasposizioni
Il sistema prova tutte le trasposizioni da −12 a +12 semitoni, cioè un’intera ottava.
Questo deriva dal fatto che l’orecchio umano percepisce come equivalenti le melodie che differiscono
solo per ottava.
### 3.2 Distanza di Levenshtein
Per confrontare due sequenze viene utilizzata la **edit distance**.
Matematicamente, è una funzione che misura il costo minimo per trasformare una sequenza in un’altra
tramite: 
- inserimenti
- cancellazioni
- sostituzioni
La distanza viene poi normalizzata per ottenere un valore comparabile.

# 4. Parte informatica: progettazione del sistema
## 4.1 Struttura modulare
Il progetto è diviso in moduli: 
- rappresentazione
- confronto
- interfaccia grafica
### 4.2 Uso dei file init.py
I file __init__.py indicano a Python che una cartella è un pacchetto.
La loro presenza permette: 
- importazioni corrette
- organizzazione del codice
- estendibilità futura
### 4.3. Interfaccia grafica
L’interfaccia rende il sistema utilizzabile anche senza conoscenze di programmazione.
Mostra: 
- verdetto
- percentuale di similarità
- confidenza
- trasposizione
- dettagli per rappresentazione
  
# Conclusione
Il progetto dimostra che la musica può essere: 
- descritta matematicamente
- analizzata algoritmicamente
- interpretata informaticamente
