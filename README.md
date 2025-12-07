# Wahl-Chatbot – Politischer Chatbot zur Parteieninformation

## Projektbeschreibung
Der **Wahl-Chatbot** ist ein Prototyp, der Benutzer:innen ermöglicht, Fragen zu fiktiven politischen Parteien zu stellen.  
Ziel des Projekts ist es, **Algorithmic Accountability** zu untersuchen und zu zeigen, wie KI-basierte Systeme auf politische Fragen neutral und sachlich antworten können.  

Das Projekt wird im Rahmen des Seminars *„Kann Code Verantwortung? Wie man Algorithmic Accountability untersucht und vermittelt?“* entwickelt.

---

## Parteien im Prototyp
1. **Fortschrittspartei**  
   *Slogan:* „Innovation und Zukunft für alle“  
   Fokus: Technologie, Digitalisierung, erneuerbare Energien, MINT-Bildung.

2. **Bewahrungspartei**  
   *Slogan:* „Tradition bewahren, Werte schützen“  
   Fokus: Konservative Werte, stabile Wirtschaft, klassische Bildung.

3. **Ökologische Partei**  
   *Slogan:* „Nachhaltigkeit jetzt“  
   Fokus: Umwelt, Klimaschutz, erneuerbare Energien.

4. **Soziale Gerechtigkeitspartei**  
   *Slogan:* „Gleichheit und Chancengleichheit für alle“  
   Fokus: Soziale Sicherheit, Umverteilung, faire Bildung, Solidarität.

---

## Features
- 🤖 **Intelligenter Chatbot** - Beantwortet Fragen zu den Parteien basierend auf strukturierter Wissensbasis
- 💡 **15 Beispiel-Fragen** - Vordefinierte Fragen zur einfachen Nutzung
- 📜 **Chat-Verlauf** - Speichert vorherige Konversationen mit Verlaufsansicht
- 📱 **Responsive Design** - Optimiert für Desktop, Tablet und Mobile
- 🎯 **Neutrale Antworten** - System-Prompt gewährleistet sachliche, unparteiische Informationen
- ✅ **Input-Validierung** - Maximale Nachrichtenlänge, Chat-History-Limits
- 📊 **Umfassendes Logging** - Detaillierte Logs für Debugging und Monitoring
- 🔧 **Zentrale Konfiguration** - Einfache Verwaltung über `.env` und `config.py`
- 🛡️ **Fehlerbehandlung** - Robuste Error-Handling-Mechanismen
- 🐳 **Docker-Support** - Containerisiert für einfaches Deployment

---

## Verwendete Tools & Technologien
- **Python 3.11+**: Backend-Logik und API-Server  
- **Flask**: Webframework für RESTful API  
- **Flask-CORS**: Erlaubt Kommunikation zwischen Frontend und Backend  
- **OpenAI API**: GPT-4 für KI-Antworten  
- **Gunicorn**: WSGI-Server für Produktion
- **dotenv**: Laden von Umgebungsvariablen, insbesondere OpenAI API Key  
- **HTML/CSS/JS**: Frontend, Chatfenster, Chatverlauf, Beispiel-Fragen  
- **Visual Studio Code**: Entwicklung und Live Server für Frontend-Test  
- **Git/GitHub**: Versionskontrolle und Team-Kollaboration
- **Fly.io**: Cloud-Deployment-Plattform
- **Docker**: Containerisierung für Deployment

---

## Projektstruktur
```
Wahl-Chatbot/
├── .dockerignore                # Docker-Ausschlussliste
├── .gitignore                   # Git-Ausschlussliste
├── DEPLOYMENT.md                # Fly.io Deployment-Anleitung
├── Dockerfile                   # Docker-Container-Konfiguration
├── fly.toml                     # Fly.io App-Konfiguration
├── requirements.txt             # Python-Abhängigkeiten
├── backend/
│   ├── app.py                   # Flask Backend-Server mit Validierung & Logging
│   ├── config.py                # Zentrale Konfigurationsverwaltung
│   ├── utils.py                 # Logger und Hilfsfunktionen
│   └── openai_test.py           # Umfassendes Testscript für API & Konfiguration
├── data/
│   ├── knowledge_base.json      # Wissensbasis: Parteienpositionen nach Themen
│   ├── parties_info.json        # Name, Slogan und Beschreibung der Parteien
│   ├── faqs.json                # Beispiel-Fragen für den Chatbot (15 Fragen)
│   └── system_prompt.txt        # System-Prompt für den KI-Chatbot
└── frontend/
    ├── index.html               # Hauptseite des Chatbots
    ├── app.js                   # Frontend-Logik (Chat, Verlauf, Vorschläge)
    └── style.css                # Styling für Chat und Layout
```

---

## Installation & Setup

### 1. Repository klonen
```bash
git clone https://github.com/ayoub5262/Wahl-Chatbot.git
cd Wahl-Chatbot
```

### 2. (Optional) Virtuelle Umgebung erstellen
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# oder
source venv/bin/activate  # Mac/Linux
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen einrichten
```bash
# Kopiere die Beispiel-Datei
copy .env.example .env   # Windows
# oder
cp .env.example .env     # Mac/Linux

# Bearbeite .env und füge deinen OpenAI API Key hinzu
# OPENAI_API_KEY=sk-your-api-key-here
```

### 5. (Optional) Konfiguration testen
```bash
# Teste API-Verbindung, Konfiguration und Datenfiles
python backend/openai_test.py
```

### 6. Backend starten
```bash
python backend/app.py
```
- Der Flask-Server läuft auf `http://127.0.0.1:5000`
- Logs werden in der Konsole und in `app.log` gespeichert
- Dank absoluter Pfade kann das Backend von jedem Verzeichnis aus gestartet werden

### 7. Frontend öffnen
- Öffnen Sie `http://127.0.0.1:5000` in Ihrem Browser
- Der Server stellt automatisch das Frontend bereit

### 8. Chatbot nutzen
- 💬 Stellen Sie eine eigene Frage oder wählen Sie eine Beispielfrage aus der rechten Seitenleiste
- 📚 Der Chatbot antwortet neutral und sachlich basierend auf der Wissensbasis
- 🔄 Nutzen Sie "Neuer Chat" um eine frische Konversation zu starten
- 📂 Der Verlauf wird in der linken Seitenleiste gespeichert und kann jederzeit abgerufen werden

---

## 🔧 Konfiguration

Die Anwendung kann über Umgebungsvariablen in der `.env` Datei konfiguriert werden:

```env
# OpenAI Konfiguration
OPENAI_API_KEY=your_api_key_here    # Erforderlich
OPENAI_MODEL=gpt-4                  # Standard: gpt-4
TEMPERATURE=0.7                     # Standard: 0.7
MAX_TOKENS=500                      # Standard: 500

# Server Konfiguration
PORT=5000                           # Standard: 5000
DEBUG=False                         # Standard: False
```

### Validierung & Limits
- **Max. Nachrichtenlänge:** 1000 Zeichen
- **Max. Chat-History:** 50 Einträge
- **Automatische Validierung** aller Eingaben
- **Logging** in `app.log` und Konsole

---

## 🧪 Testing

Teste die API-Verbindung und Konfiguration:

```bash
python backend/openai_test.py
```

Das Testscript prüft:
- ✅ Konfigurationsvalidierung
- ✅ Existenz und Validität aller Datenfiles
- ✅ OpenAI API-Verbindung
- ✅ Funktionalität mit Test-Anfrage

---

## Nutzungshinweise
- 🎯 **Neutrale Wissensbasis** - Alle Antworten basieren ausschließlich auf vordefinierten Daten
- ℹ️ **Begrenzte Informationen** - Bei unbekannten Fragen wird höflich auf fehlende Informationen hingewiesen
- 🤐 **Keine Meinungen** - Der Bot gibt keine persönlichen Empfehlungen ab
- 📊 **Faktenbasiert** - Nur objektive Informationen aus der Wissensbasis

---

## 📌 Technische Verbesserungen

Das Projekt wurde mit folgenden Best Practices optimiert:

### Backend-Architektur
- ✅ **Zentrale Konfiguration** (`backend/config.py`) - Alle Einstellungen an einem Ort
- ✅ **Strukturiertes Logging** (`backend/utils.py`) - Console & File-Logging
- ✅ **Input-Validierung** - Schutz vor ungültigen/zu langen Eingaben
- ✅ **Error Handling** - Umfassende Try-Catch-Blöcke mit aussagekräftigen Fehlermeldungen
- ✅ **Modulare Struktur** - Wiederverwendbare Komponenten

### Sicherheit & Validierung
- 🔒 API-Key über Umgebungsvariablen (nie im Code)
- ✅ Request-Validierung (Typ, Länge, Format)
- 🛡️ Error-Handling für API-Ausfälle
- 📝 Audit-Trail durch detailliertes Logging

### Code-Qualität
- 📚 Dokumentierte Funktionen mit Docstrings
- 🎯 Klare Trennung von Daten, Logik und Präsentation
- 🔧 Testscript für schnelle Validierung
- 📦 Docker-Ready für einfaches Deployment

---

## 📌 Hinweise zu Algorithmic Accountability
- Der Chatbot ist **neutral** konzipiert, um Bias zu vermeiden
- Alle Antworten basieren ausschließlich auf der vordefinierten Wissensbasis
- Transparente Datenstruktur ermöglicht Nachvollziehbarkeit der Antworten
- Projekt dient zur Untersuchung von **Algorithmic Accountability** im politischen Kontext

---

## 🤝 Mitwirken

Verbesserungsvorschläge sind willkommen! Bei Problemen oder Fragen:
1. Nutze `python backend/openai_test.py` für Diagnose
2. Prüfe die Logs in `app.log`
3. Stelle sicher, dass `.env` korrekt konfiguriert ist

---

## 📄 Lizenz
Dieses Projekt ist für Bildungs- und Seminarzwecke erstellt.
