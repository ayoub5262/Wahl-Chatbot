"""
Analyse des strukturellen Reihenfolge-Bias in der Wissensbasis
Unabhängig vom Inhalt - nur technische Struktur
"""

import json
from collections import Counter
import numpy as np

def analyze_party_order_bias(kb_path='../data/knowledge_base.json'):
    """Analysiert strukturellen Reihenfolge-Bias in der Wissensbasis"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    party_positions = {
        "Fortschrittspartei": [],
        "Bewahrungspartei": [],
        "Ökologische Partei": [],
        "Soziale Gerechtigkeitspartei": []
    }
    
    # Erfasse Position jeder Partei in jedem Thema
    for topic, parties in kb.items():
        party_list = list(parties.keys())
        for party, position in zip(party_list, range(len(party_list))):
            party_positions[party].append(position)
    
    # Statistik ausgeben
    print("=" * 60)
    print("STRUKTURELLER REIHENFOLGE-BIAS ANALYSE")
    print("=" * 60)
    print()
    
    for party, positions in party_positions.items():
        avg_pos = sum(positions) / len(positions)
        print(f"{party}:")
        print(f"  Durchschnittliche Position: {avg_pos:.2f}")
        print(f"  Häufigkeit Position 0 (erste): {positions.count(0)}")
        print(f"  Häufigkeit Position 1: {positions.count(1)}")
        print(f"  Häufigkeit Position 2: {positions.count(2)}")
        print(f"  Häufigkeit Position 3 (letzte): {positions.count(3)}")
        print(f"  Positionsverteilung: {dict(Counter(positions))}")
        print()
    
    return party_positions


def demonstrate_primacy_recency_effect(kb_path='../data/knowledge_base.json'):
    """
    Zeigt wie die feste Reihenfolge in der KB psychologische Bias erzeugt
    
    Primacy Effect: Erste Information wird stärker erinnert
    Recency Effect: Letzte Information wird stärker erinnert
    """
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    print("=" * 60)
    print("PRIMACY & RECENCY EFFECT")
    print("=" * 60)
    print()
    print("Aktuelle Struktur (immer gleiche Reihenfolge):")
    print()
    
    for topic in list(kb.keys())[:5]:  # Erste 5 Themen als Beispiel
        parties = list(kb[topic].keys())
        print(f"{topic}:")
        print(f"  1. {parties[0]} <- PRIMACY (bevorzugt)")
        print(f"  2. {parties[1]}")
        print(f"  3. {parties[2]}")
        print(f"  4. {parties[3]} <- RECENCY (bevorzugt)")
        print()
    
    # Zeige Konsequenz
    first_party = list(kb["Umwelt"].keys())[0]
    last_party = list(kb["Umwelt"].keys())[-1]
    
    print("⚠️  BIAS-RISIKO:")
    print(f"   '{first_party}' erscheint IMMER zuerst")
    print(f"   '{last_party}' erscheint IMMER zuletzt")
    print("   → Nutzer könnten systematisch diese Parteien bevorzugen/benachteiligen")
    print()


def calculate_structural_neutrality_score(kb_path='../data/knowledge_base.json'):
    """Berechnet Neutralitäts-Score basierend auf Struktur"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    parties = ["Fortschrittspartei", "Bewahrungspartei", 
               "Ökologische Partei", "Soziale Gerechtigkeitspartei"]
    
    position_counts = {party: [] for party in parties}
    
    for topic, party_dict in kb.items():
        party_list = list(party_dict.keys())
        for party in parties:
            if party in party_list:
                position_counts[party].append(party_list.index(party))
    
    # Berechne Standardabweichung der Positionen
    print("=" * 60)
    print("NEUTRALITÄTS-METRIKEN")
    print("=" * 60)
    print()
    
    ideal_avg = 1.5  # Bei 4 Parteien: (0+1+2+3)/4 = 1.5
    ideal_std = 1.118  # Standardabweichung bei perfekter Gleichverteilung
    
    bias_scores = []
    
    for party, positions in position_counts.items():
        std_dev = np.std(positions)
        avg = np.mean(positions)
        bias_score = abs(avg - ideal_avg)
        bias_scores.append(bias_score)
        
        print(f"{party}:")
        print(f"  Durchschnitt: {avg:.2f} (Ideal: {ideal_avg})")
        print(f"  Standardabweichung: {std_dev:.2f} (Ideal: ~{ideal_std:.2f})")
        print(f"  Bias-Score: {bias_score:.2f} (0 = perfekt neutral)")
        print()
    
    # Gesamtscore
    overall_bias = np.mean(bias_scores)
    print(f"Gesamt-Bias-Score: {overall_bias:.3f}")
    print("(0 = strukturell neutral, höher = mehr Bias)")
    print()
    
    # Interpretation
    if overall_bias < 0.1:
        print("✓ AUSGEZEICHNET: Struktur ist nahezu perfekt neutral")
    elif overall_bias < 0.5:
        print("✓ GUT: Struktur zeigt minimalen Bias")
    elif overall_bias < 1.0:
        print("⚠ WARNUNG: Signifikanter struktureller Bias vorhanden")
    else:
        print("❌ KRITISCH: Starker struktureller Bias - Randomisierung empfohlen")
    print()


def main():
    """Führt alle Analysen durch"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  STRUKTURELLER BIAS-ANALYSE DER WISSENSBASIS".center(58) + "║")
    print("║" + "  (Unabhängig vom Inhalt)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Analyse 1: Reihenfolge-Bias
    analyze_party_order_bias()
    
    # Analyse 2: Primacy & Recency Effect
    demonstrate_primacy_recency_effect()
    
    # Analyse 3: Neutralitäts-Metriken
    calculate_structural_neutrality_score()
    
    print("=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    print()
    print("Die Analyse zeigt, dass die technische Struktur der JSON-Datei")
    print("einen systematischen Bias erzeugen kann, wenn:")
    print()
    print("1. Die Reihenfolge der Parteien in allen Themen GLEICH ist")
    print("2. Keine Randomisierung bei der Präsentation erfolgt")
    print("3. Nutzer immer die gleiche Anordnung sehen")
    print()
    print("EMPFEHLUNG:")
    print("→ Implementieren Sie Randomisierung in der Präsentationsschicht")
    print("→ Dokumentieren Sie die ursprüngliche Reihenfolge für Logging")
    print("→ Messen Sie Nutzerverhalten mit/ohne Randomisierung")
    print()


if __name__ == "__main__":
    main()
