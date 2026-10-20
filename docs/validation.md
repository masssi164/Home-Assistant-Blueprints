# Teststand

## Öffentliche Beta v1.0.0-beta.1

Der End-to-End-Ablauf der neuen Blueprint-Skripte wurde in Home Assistant mit einem
**Siemens TP516DX3** erfolgreich getestet: Einrichtung der Blueprints, Konfiguration
der Zentrale und Favoriten sowie reale Kaffeezubereitung über die Home-Connect-Anbindung.
Die bestehende Kaffee-Steuerung funktioniert nach der Umstellung weiterhin.

Dieser Gerätetest gilt für die getestete Installation. Weitere Modelle, Programme
und Rezeptkombinationen werden mit ihrem jeweiligen Testumfang ergänzt; die Beta
behauptet keine universelle Gerätekompatibilität.

## Automatisierte Prüfungen

Die Tests lesen die ausgelieferten YAML-Dateien. Geprüft werden unter anderem
YAML/JSON, doppelte Schlüssel, Blueprint-Inputs, Jinja-Syntax, Laufzeit-Defaults,
Typen, erlaubte Optionen, Gerätezuordnung, Trockenlauf, Einschalten, Verbindung,
Fernstartfreigabe, lokale Bedienung, Zustände und simulierte Fehler-/Wartepfade.
Hinzu kommen Rezeptweitergabe, Dashboard-Mapping und Statistikfälle,
Dokumentationslinks und Datenschutzheuristiken.

Die Simulationsumgebung ersetzt nicht die reale Home-Assistant-Laufzeit,
Cloud-API oder Geräteausgabe. Deshalb werden automatisierte Prüfungen und reale
Gerätetests getrennt dokumentiert.

### Nachweis vor der Beta-Veröffentlichung

[Actions-Lauf 39375079858](https://github.com/masssi164/Home-Assistant-Blueprints/actions/runs/39375079858)
für Commit `805f17cfb3b4353149abebc3d0e8d8dab204448a` wurde erfolgreich abgeschlossen.

Historischer Teststand vom 18. Oktober 2026:

- Statische/Simulationsprüfungen: 102 Tests bestanden mit Python 3.13.
- Home-Assistant-Schemas: 2 Tests bestanden gegen 2026.10.2 mit Python 3.14.

[Historischer Actions-Lauf 39162471240](https://github.com/masssi164/Home-Assistant-Blueprints/actions/runs/39162471240).

### Prüfung des Release-Commits

Der Workflow [Publish beta release](https://github.com/masssi164/Home-Assistant-Blueprints/actions/workflows/release-beta.yml)
führt beide Prüfgruppen auf dem Release-Commit aus und veröffentlicht nur, wenn
beide erfolgreich sind. Die zugehörigen Actions-Protokolle enthalten die Ergebnisse
und Testzahlen des konkreten Release-Stands.

Die Änderungen für die Beta betreffen Dokumentation, Versions-/Quellverweise und
Veröffentlichung. Die Zubereitungslogik und ihre Standardwerte bleiben unverändert.

## Weitere Gerätetests

Für zusätzliche Modelle und Interfaces die [Testcheckliste](acceptance.md) verwenden.
Versionsnummern, Firmwarestände oder einzelne Rezeptgrenzen nur eintragen, wenn sie
für den jeweiligen Test tatsächlich bekannt sind. Fehlerpfade während heißer
Getränkeausgabe nicht durch riskante Manipulation erzwingen.

[Quellen](sources.md)
