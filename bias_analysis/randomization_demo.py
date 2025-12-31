"""
Demonstration: Vergleich zwischen fester und randomisierter Struktur
Zeigt wie Randomisierung strukturellen Bias eliminiert
"""

import json
import random
from collections import defaultdict

def get_fixed_order_response(topic, kb):
    """Gibt Antworten in fester Reihenfolge zurück (wie aktuell)"""
    if topic not in kb:
        return None, []
    
    party_info = kb[topic]
    parties = list(party_info.keys())
    
    return party_info, parties


def get_randomized_response(topic, kb):
    """Gibt Antworten in zufälliger Reihenfolge zurück"""
    if topic not in kb:
        return None, []
    
    party_info = kb[topic]
    parties = list(party_info.keys())
    
    # Randomisiere Reihenfolge
    random.shuffle(parties)
    
    # Erstelle neue Ordnung
    randomized_info = {party: party_info[party] for party in parties}
    
    return randomized_info, parties


def compare_structures(kb_path='../data/knowledge_base.json'):
    """Vergleicht feste vs. randomisierte Struktur"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    topic = "Umwelt"
    
    print("=" * 60)
    print("VERGLEICH: FESTE vs. RANDOMISIERTE STRUKTUR")
    print("=" * 60)
    print()
    
    print("SZENARIO A: FESTE STRUKTUR (AKTUELL)")
    print("-" * 60)
    print(f"Thema: {topic}")
    print()
    
    _, parties_fixed = get_fixed_order_response(topic, kb)
    for i, party in enumerate(parties_fixed, 1):
        print(f"  {i}. {party}")
    
    print()
    print("⚠️  Problem: IMMER die gleiche Reihenfolge!")
    print("   → Primacy Effect begünstigt:", parties_fixed[0])
    print("   → Recency Effect begünstigt:", parties_fixed[-1])
    print()
    
    print("\n" + "=" * 60)
    print("SZENARIO B: RANDOMISIERTE STRUKTUR (EMPFOHLEN)")
    print("-" * 60)
    print(f"Thema: {topic}")
    print()
    print("Beispiel: 5 verschiedene Nutzer bekommen unterschiedliche Reihenfolgen:\n")
    
    for user_num in range(1, 6):
        _, parties_random = get_randomized_response(topic, kb)
        print(f"Nutzer {user_num}:")
        for i, party in enumerate(parties_random, 1):
            print(f"  {i}. {party}")
        print()
    
    print("✓ Vorteil: Keine systematische Bevorzugung!")
    print("  → Jede Partei erscheint gleich oft auf jeder Position")
    print()


def simulate_user_choices(num_simulations=1000, kb_path='../data/knowledge_base.json'):
    """
    Simuliert Nutzerwahl mit Primacy Effect
    Annahme: 40% wählen erste Option, 30% zweite, 20% dritte, 10% vierte
    """
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    topic = "Umwelt"
    
    # Feste Struktur
    fixed_choices = defaultdict(int)
    for _ in range(num_simulations):
        _, parties = get_fixed_order_response(topic, kb)
        # Simuliere Primacy Effect
        choice = random.choices(range(4), weights=[40, 30, 20, 10])[0]
        fixed_choices[parties[choice]] += 1
    
    # Randomisierte Struktur
    random_choices = defaultdict(int)
    for _ in range(num_simulations):
        _, parties = get_randomized_response(topic, kb)
        # Simuliere Primacy Effect (gleiche Gewichtung)
        choice = random.choices(range(4), weights=[40, 30, 20, 10])[0]
        random_choices[parties[choice]] += 1
    
    print("\n" + "=" * 60)
    print(f"SIMULATION: {num_simulations} NUTZERWAHLEN")
    print("=" * 60)
    print()
    print("Annahme: Nutzer bevorzugen erste Optionen (Primacy Effect)")
    print("         40% wählen 1. Option, 30% → 2., 20% → 3., 10% → 4.")
    print()
    
    print("ERGEBNIS MIT FESTER STRUKTUR:")
    print("-" * 60)
    for party in sorted(fixed_choices.keys()):
        percentage = (fixed_choices[party] / num_simulations) * 100
        bar = "█" * int(percentage / 2)
        print(f"{party:30s}: {fixed_choices[party]:4d} ({percentage:5.1f}%) {bar}")
    
    print()
    print("ERGEBNIS MIT RANDOMISIERUNG:")
    print("-" * 60)
    for party in sorted(random_choices.keys()):
        percentage = (random_choices[party] / num_simulations) * 100
        bar = "█" * int(percentage / 2)
        print(f"{party:30s}: {random_choices[party]:4d} ({percentage:5.1f}%) {bar}")
    
    print()
    print("INTERPRETATION:")
    print("-" * 60)
    print("• Mit fester Struktur: Eine Partei wird systematisch bevorzugt")
    print("• Mit Randomisierung: Alle Parteien erhalten ~25% der Stimmen")
    print("• Randomisierung neutralisiert den Primacy/Recency Effect!")
    print()


def main():
    """Führt alle Demonstrationen durch"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  DEMONSTRATION: RANDOMISIERUNG vs. FESTE STRUKTUR".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    compare_structures()
    simulate_user_choices(num_simulations=1000)
    
    print("=" * 60)
    print("FAZIT")
    print("=" * 60)
    print()
    print("Die technische Struktur der JSON-Datei ist NICHT das Problem.")
    print("Das Problem ist die FEHLENDE RANDOMISIERUNG bei der Präsentation.")
    print()
    print("EMPFEHLUNG:")
    print("1. JSON-Datei kann so bleiben (alphabetisch o.ä. sortiert)")
    print("2. Bei JEDER Nutzer-Anfrage die Reihenfolge randomisieren")
    print("3. Original-Reihenfolge für Logging speichern")
    print("4. A/B-Test durchführen: mit/ohne Randomisierung")
    print()


if __name__ == "__main__":
    main()
