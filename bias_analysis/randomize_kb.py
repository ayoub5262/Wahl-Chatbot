"""
Randomisiert die Reihenfolge der Parteien in der knowledge_base.json
"""

import json
import random

def randomize_knowledge_base(input_path='../data/knowledge_base.json', output_path='../data/knowledge_base.json'):
    """Randomisiert die Partei-Reihenfolge in jedem Thema"""
    
    # Lade Wissensbasis
    with open(input_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    print("Ursprüngliche Reihenfolge:")
    print("-" * 60)
    for topic in list(kb.keys())[:3]:
        parties = list(kb[topic].keys())
        print(f"{topic}: {', '.join(parties)}")
    
    # Randomisiere Reihenfolge in jedem Thema
    randomized = {}
    for topic, party_dict in kb.items():
        parties = list(party_dict.keys())
        random.shuffle(parties)
        randomized[topic] = {party: party_dict[party] for party in parties}
    
    # Speichere randomisierte Version
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(randomized, f, ensure_ascii=False, indent=2)
    
    print("\n✓ Reihenfolge randomisiert!")
    print("\nNeue Reihenfolge:")
    print("-" * 60)
    for topic in list(randomized.keys())[:3]:
        parties = list(randomized[topic].keys())
        print(f"{topic}: {', '.join(parties)}")
    
    print(f"\n✓ Datei gespeichert: {output_path}")

if __name__ == "__main__":
    randomize_knowledge_base()
