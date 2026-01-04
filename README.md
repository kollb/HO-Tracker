# BBk Home Office Tracker (Standalone)

Ein leichtgewichtiges Tool zur Erfassung von Home Office- und Bürozeiten, das direkt im Browser läuft. Es benötigt **keine Installation** (kein Python, kein Docker) und speichert Daten lokal auf deinem PC.

## ✨ Features

* **100% Lokal:** Läuft als einzelne HTML-Datei im Browser.
* **Datenspeicherung:** Speichert direkt in eine lokale JSON-Datei (`daten.json`) über die moderne File System Access API.
* **Intelligente Zeiterfassung:**
    * Automatische Berechnung der Netto-Arbeitszeit.
    * Spezielle Pausen-Logik (Pausenkorridor ab 6h / 9h).
    * Flexible Eingabe (z.B. `0615`, `6.15` oder `06:15`).
* **Übersicht:**
    * Monatsansicht als Liste oder Kalender.
    * Home Office Quote (Budget-Balken).
    * Wochensummen (Ist vs. Soll).
* **Feiertage:** Automatische Erkennung (Hessen) + Möglichkeit für eigene/betriebliche Feiertage.

## 🚀 Installation & Start

1.  **Datei vorbereiten:**
    Erstelle an einem Ort deiner Wahl eine leere Textdatei und nenne sie `daten.json`.

2.  **App starten:**
    Öffne die Datei `HO-Tracker.html` mit einem **Chromium-basierten Browser** (Google Chrome oder Microsoft Edge).

3.  **Verbinden:**
    Klicke oben rechts auf das **Ordner-Icon** 📂 und wähle deine `bbk_daten.json` aus.

4.  **Fertig:**
    Ab jetzt werden Änderungen automatisch in diese Datei gespeichert. Beim nächsten Öffnen klickst du nur noch auf "Verbinden".

## 🛠 Voraussetzungen

* **Browser:** Microsoft Edge oder Google Chrome (wegen der File System Access API).
* **Betriebssystem:** Windows, macOS oder Linux.
* **Rechte:** Keine Admin-Rechte erforderlich.
