"""
Visualisierung des strukturellen Bias in der Wissensbasis
Erstellt Heatmap und andere Visualisierungen
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def visualize_order_bias(kb_path='../data/knowledge_base.json', output_path='output/'):
    """Erstellt Heatmap zur Visualisierung der Positionierung"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Matrix erstellen: Thema x Partei-Position
    topics = list(kb.keys())
    parties = ["Fortschrittspartei", "Bewahrungspartei", 
               "Ökologische Partei", "Soziale Gerechtigkeitspartei"]
    
    position_matrix = []
    for topic in topics:
        party_list = list(kb[topic].keys())
        row = [party_list.index(party) for party in parties]
        position_matrix.append(row)
    
    df = pd.DataFrame(position_matrix, columns=parties, index=topics)
    
    # Heatmap erstellen
    plt.figure(figsize=(12, 10))
    sns.heatmap(df, annot=True, fmt='d', cmap='RdYlGn_r', 
                cbar_kws={'label': 'Position (0=erste, 3=letzte)'},
                linewidths=0.5, linecolor='gray')
    plt.title('Struktureller Reihenfolge-Bias in der Wissensbasis\n(Je roter, desto früher erscheint die Partei)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Partei', fontsize=12)
    plt.ylabel('Thema', fontsize=12)
    plt.tight_layout()
    
    output_file = output_path + 'structural_bias_heatmap.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Heatmap gespeichert: {output_file}")
    plt.close()


def visualize_position_distribution(kb_path='../data/knowledge_base.json', output_path='output/'):
    """Erstellt Balkendiagramm der Positionsverteilung"""
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    parties = ["Fortschrittspartei", "Bewahrungspartei", 
               "Ökologische Partei", "Soziale Gerechtigkeitspartei"]
    
    position_counts = {party: [0, 0, 0, 0] for party in parties}
    
    for topic, party_dict in kb.items():
        party_list = list(party_dict.keys())
        for party in parties:
            if party in party_list:
                pos = party_list.index(party)
                position_counts[party][pos] += 1
    
    # Balkendiagramm erstellen
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(4)
    width = 0.2
    
    for i, (party, counts) in enumerate(position_counts.items()):
        offset = (i - 1.5) * width
        ax.bar(x + offset, counts, width, label=party)
    
    ax.set_xlabel('Position', fontsize=12)
    ax.set_ylabel('Häufigkeit', fontsize=12)
    ax.set_title('Verteilung der Parteien über Positionen\n(Idealer Fall: Alle Balken gleich hoch)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['1. Position\n(Primacy)', '2. Position', '3. Position', '4. Position\n(Recency)'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Ideal-Linie hinzufügen
    ideal_value = len(kb) / 4  # Jede Partei sollte in jeder Position gleich oft vorkommen
    ax.axhline(y=ideal_value, color='red', linestyle='--', linewidth=2, label='Ideal (neutral)')
    
    plt.tight_layout()
    
    output_file = output_path + 'position_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Positionsverteilung gespeichert: {output_file}")
    plt.close()


def visualize_average_positions(kb_path='../data/knowledge_base.json', output_path='output/'):
    """Zeigt durchschnittliche Position jeder Partei"""
    
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
    
    # Durchschnitt berechnen
    avg_positions = {party: np.mean(positions) for party, positions in position_counts.items()}
    std_positions = {party: np.std(positions) for party, positions in position_counts.items()}
    
    # Balkendiagramm
    fig, ax = plt.subplots(figsize=(10, 6))
    
    parties_sorted = sorted(avg_positions.keys(), key=lambda x: avg_positions[x])
    avgs = [avg_positions[p] for p in parties_sorted]
    stds = [std_positions[p] for p in parties_sorted]
    
    colors = ['green' if abs(avg - 1.5) < 0.1 else 'orange' if abs(avg - 1.5) < 0.5 else 'red' 
              for avg in avgs]
    
    bars = ax.barh(parties_sorted, avgs, xerr=stds, color=colors, alpha=0.7)
    
    # Ideal-Linie
    ax.axvline(x=1.5, color='blue', linestyle='--', linewidth=2, label='Ideal (1.5)')
    
    ax.set_xlabel('Durchschnittliche Position', fontsize=12)
    ax.set_ylabel('Partei', fontsize=12)
    ax.set_title('Durchschnittliche Position jeder Partei über alle Themen\n(Je näher an 1.5, desto neutraler)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, 3)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
    ax.grid(axis='x', alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    output_file = output_path + 'average_positions.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Durchschnittliche Positionen gespeichert: {output_file}")
    plt.close()


def main():
    """Erstellt alle Visualisierungen"""
    print("\n" + "=" * 60)
    print("VISUALISIERUNG DES STRUKTURELLEN BIAS")
    print("=" * 60 + "\n")
    
    try:
        visualize_order_bias()
        visualize_position_distribution()
        visualize_average_positions()
        
        print("\n" + "=" * 60)
        print("✓ Alle Visualisierungen erfolgreich erstellt!")
        print("  Siehe Ordner: bias_analysis/output/")
        print("=" * 60 + "\n")
        
    except ImportError as e:
        print(f"\n❌ Fehler: {e}")
        print("\nBitte installieren Sie die benötigten Pakete:")
        print("  pip install matplotlib seaborn pandas numpy")
        print()


if __name__ == "__main__":
    main()
