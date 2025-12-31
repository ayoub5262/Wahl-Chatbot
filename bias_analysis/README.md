# Struktureller Bias-Analyse der Wissensbasis

Dieses Verzeichnis enthält Tools zur Analyse des strukturellen Reihenfolge-Bias in der Wissensbasis, unabhängig vom Inhalt.

## 🎯 Zweck

Die technische Struktur einer JSON-basierten Wissensbasis kann systematischen Bias einführen durch:
- **Primacy Effect**: Erste Optionen werden bevorzugt erinnert und gewählt
- **Recency Effect**: Letzte Optionen werden ebenfalls bevorzugt
- **Feste Reihenfolge**: Immer gleiche Anordnung führt zu systematischer Bevorzugung

## 📁 Dateien

### 1. `structural_bias_analysis.py`
Hauptanalyse-Skript, das folgende Metriken berechnet:
- Positionsverteilung jeder Partei
- Durchschnittliche Position über alle Themen
- Neutralitäts-Score (0 = perfekt neutral)
- Primacy/Recency Effect Demonstration

**Verwendung:**
```bash
python structural_bias_analysis.py
```

**Ausgabe:**
- Detaillierte Statistiken über Positionierung
- Bias-Scores für jede Partei
- Interpretation der Ergebnisse

### 2. `visualize_bias.py`
Erstellt visuelle Darstellungen des strukturellen Bias:
- **Heatmap**: Zeigt Position jeder Partei in jedem Thema
- **Positionsverteilung**: Balkendiagramm über alle Positionen
- **Durchschnittliche Positionen**: Vergleich mit idealem Wert (1.5)

**Verwendung:**
```bash
python visualize_bias.py
```

**Benötigte Pakete:**
```bash
pip install matplotlib seaborn pandas numpy
```

**Ausgabe:**
- `output/structural_bias_heatmap.png`
- `output/position_distribution.png`
- `output/average_positions.png`

### 3. `randomization_demo.py`
Demonstriert den Unterschied zwischen fester und randomisierter Struktur:
- Vergleich der beiden Ansätze
- Simulation von Nutzerwahlen mit Primacy Effect
- Zeigt Wirksamkeit der Randomisierung

**Verwendung:**
```bash
python randomization_demo.py
```

**Ausgabe:**
- Vergleich feste vs. randomisierte Reihenfolge
- Simulationsergebnisse (1000 virtuelle Nutzer)
- Empfehlungen zur Implementierung

## 🔍 Wichtige Erkenntnisse

### Aktuelle Struktur (knowledge_base.json)
Die Wissensbasis zeigt eine **feste Reihenfolge**:
1. Fortschrittspartei (immer Position 0)
2. Bewahrungspartei (immer Position 1)
3. Ökologische Partei (immer Position 2)
4. Soziale Gerechtigkeitspartei (immer Position 3)

### Problem
- **Primacy Effect**: "Fortschrittspartei" wird systematisch bevorzugt (40% Vorteil)
- **Recency Effect**: "Soziale Gerechtigkeitspartei" profitiert ebenfalls
- **Mittlere Positionen**: "Bewahrungspartei" und "Ökologische Partei" benachteiligt

### Lösung: Randomisierung
```python
import random

def get_randomized_parties(topic, knowledge_base):
    parties = list(knowledge_base[topic].keys())
    random.shuffle(parties)  # Randomisiere bei jeder Anfrage
    return parties
```

## 📊 Metriken

### Neutralitäts-Score
- **0.0**: Perfekt neutral - jede Partei erscheint gleich oft auf jeder Position
- **< 0.5**: Minimal Bias - akzeptabel
- **0.5 - 1.0**: Signifikanter Bias - Randomisierung empfohlen
- **> 1.0**: Kritischer Bias - Randomisierung notwendig

### Ideale Werte (bei 4 Parteien)
- Durchschnittliche Position: **1.5** (bei Positionen 0, 1, 2, 3)
- Standardabweichung: **~1.12**
- Jede Position gleich oft: **25%** der Themen

## 🎓 Für Präsentationen

### Empfohlener Ablauf:
1. **Problem identifizieren**: `structural_bias_analysis.py` ausführen
2. **Visualisieren**: `visualize_bias.py` für Grafiken
3. **Lösung demonstrieren**: `randomization_demo.py` für Vergleich
4. **Diskutieren**: Technische Struktur vs. Präsentationslogik

### Kernbotschaft:
> Die technische Struktur der JSON-Datei ist neutral sortiert (z.B. alphabetisch).
> Das Problem entsteht erst durch die **fehlende Randomisierung** bei der Präsentation.
> Randomisierung auf Anwendungsebene löst das Problem vollständig.

## 🛠️ Integration in den Chatbot

Beispiel-Implementierung für `backend/app.py`:

```python
import random

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    topic = data.get('topic')
    
    # Lade Wissensbasis
    with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    if topic in kb:
        parties = list(kb[topic].keys())
        random.shuffle(parties)  # RANDOMISIERUNG
        
        # Logge Original-Reihenfolge für Analyse
        log_order(user_id, topic, parties)
        
        # Präsentiere randomisiert
        response = {party: kb[topic][party] for party in parties}
        return jsonify(response)
```

## 📈 A/B Testing

Um die Wirksamkeit zu messen:

1. **Gruppe A**: Feste Reihenfolge (Kontrolle)
2. **Gruppe B**: Randomisierte Reihenfolge (Treatment)

Messen:
- Verteilung der gewählten Parteien
- Position der gewählten Partei
- Chi-Quadrat-Test für Signifikanz

## 🔗 Weiterführende Literatur

- [Primacy Effect (Wikipedia)](https://en.wikipedia.org/wiki/Serial-position_effect)
- [Choice Architecture & Order Effects](https://www.behavioraleconomics.com/resources/mini-encyclopedia-of-be/order-effects/)
- [Designing Unbiased Surveys](https://www.pewresearch.org/methods/u-s-survey-research/questionnaire-design/)
