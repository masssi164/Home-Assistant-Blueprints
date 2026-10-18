# Änderungen

## 0.1.0-preview.1 – vorbereitet, noch nicht veröffentlicht

Aus den bereitgestellten Kaffee-Skripten und dem Barista-Dashboard abgeleitet:

- Zwei Script-Blueprints: eine gemeinsame Zentrale pro Maschine und konfigurierbare Favoriten.
- Fünf Entity-Auswahllisten; Geräte-ID automatisch ermittelt und gemeinsame Zuordnung geprüft.
- Laufzeit-Default/Validierung für Getränk und optionale Rezeptparameter.
- Gemeinsamer single-Modus bis zur beobachteten Rückkehr nach Ready; kein automatischer Start-Retry.
- Trockenlauf als Standard, automatisches Einschalten nur nach bewusster Freigabe.
- Native Quick-Start-Ansicht ohne Zusatzkarten; bereinigte optionale Mushroom-Barista-Vorlage.
- Einmaliges lokales ID-Mapping für Dashboard-Tokens statt verteilter privater IDs.
- Einsteiger-, Rezept-, Interface-, Migrations-, Fehlersuch- und Abnahmedokumentation.
- Lokale statische/Template-/Simulationsprüfungen; HA-Schema-CI vorbereitet, noch nicht ausgeführt.

Nicht enthalten: tatsächliche Hardware-Freigabe, herstellerunabhängige lokale
Geräteanbindung, Tassenerkennung, Companion-App-Bestätigung, universelle
Modellkompatibilität oder ein veröffentlichter GitHub-Release.
